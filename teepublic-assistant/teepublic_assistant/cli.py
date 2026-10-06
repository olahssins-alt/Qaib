"""Command line entry point: python -m teepublic_assistant <command> ..."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import sales

# Send at most this much raw CSV to Claude with `ask`; the summary is always sent.
RAW_CSV_LIMIT = 200_000


def _overrides(pairs: list[str] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"--col expects field=Column Name, got {pair!r}")
        key, value = pair.split("=", 1)
        if key not in sales.COLUMN_ALIASES:
            raise SystemExit(f"Unknown field {key!r}. Fields: {', '.join(sales.COLUMN_ALIASES)}")
        out[key] = value
    return out


def _load_summary(args) -> dict:
    try:
        rows = sales.load_sales(args.csv, _overrides(args.col))
    except (OSError, ValueError) as e:
        raise SystemExit(str(e))
    if not rows:
        raise SystemExit(f"No sales rows found in {args.csv}")
    return sales.summarize(rows, top_n=args.top)


def _write(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
        print(f"Saved to {out}", file=sys.stderr)
    else:
        print(text)


def cmd_report(args) -> None:
    summary = _load_summary(args)
    _write(json.dumps(summary, indent=2) if args.json else sales.format_report(summary), args.out)


def cmd_insights(args) -> None:
    from .claude import sales_insights

    summary = _load_summary(args)
    print("Asking Claude to analyze your sales…", file=sys.stderr)
    _write(sales_insights(summary, goal=args.goal), args.out)


def cmd_listing(args) -> None:
    from .claude import format_listing, write_listing

    notes = None
    if args.notes:
        notes = Path(args.notes).read_text(encoding="utf-8") if Path(args.notes).is_file() else args.notes
    if args.image and not Path(args.image).is_file():
        raise SystemExit(f"No such image: {args.image}")
    existing = None
    if args.existing:
        existing = Path(args.existing).read_text(encoding="utf-8") if Path(args.existing).is_file() else args.existing
    summary = None
    if args.csv:
        summary = _load_summary(args)
    print("Asking Claude to write the listing…", file=sys.stderr)
    listing = write_listing(notes, image=args.image, existing_listing=existing, store_summary=summary)
    _write(json.dumps(listing, indent=2) if args.json else format_listing(listing), args.out)


def cmd_research(args) -> None:
    from datetime import date

    from .claude import research_trends

    summary = _load_summary(args) if args.csv else None
    print("Claude is researching trends on the web (this can take a few minutes)…", file=sys.stderr)
    report = research_trends(args.topic, today=date.today().isoformat(), count=args.count,
                             store_summary=summary, language=args.language)
    _write(report, args.out)


def cmd_design(args) -> None:
    from .claude import make_design

    out = Path(args.out or "design.svg")
    if out.suffix.lower() != ".svg":
        raise SystemExit("--out must end in .svg")
    print("Claude is drawing the design…", file=sys.stderr)
    svg = make_design(args.concept, colors=args.colors, shirt_color=args.shirt_color)
    out.write_text(svg, encoding="utf-8")
    print(f"Saved {out}", file=sys.stderr)
    if args.png:
        try:
            import cairosvg
        except ImportError:
            raise SystemExit("Install cairosvg (pip install cairosvg) to export PNG, or open the SVG in Inkscape and export it.")
        png = out.with_suffix(".png")
        cairosvg.svg2png(url=str(out), write_to=str(png), output_width=4500, output_height=5500)
        print(f"Saved {png} (4500x5500, transparent)", file=sys.stderr)


def cmd_keywords(args) -> None:
    from . import keywords as kw

    if args.kw_command == "init":
        kw.init_file(args.file)
        print(f"Created {args.file}. Open it in Excel/Google Sheets, or add rows with `keywords add`.", file=sys.stderr)
    elif args.kw_command == "add":
        if not Path(args.file).exists():
            kw.init_file(args.file)
        done = kw.add_keywords(args.file, args.keyword, teepublic=args.teepublic, etsy=args.etsy)
        print(f"Saved {len(done)} keyword(s) to {args.file}", file=sys.stderr)
    elif args.kw_command == "trends":
        if not Path(args.file).exists():
            kw.init_file(args.file)
        for trends_csv in args.trends_csv:
            for row in kw.import_trends(args.file, trends_csv):
                growth = f"{row['trend_growth']}x vs last year" if row["trend_growth"] else "no year-ago data"
                print(f"  {row['keyword']}: recent {row['trend_recent']}/100, {growth}, peak {row['peak_month'] or '?'}",
                      file=sys.stderr)
        print(f"Updated {args.file}", file=sys.stderr)
    elif args.kw_command == "score":
        scored = kw.score_rows(kw.read_file(args.file))
        if args.json:
            text = json.dumps([{k: v for k, v in r.items() if not k.startswith("_")} for r in scored], indent=2)
        else:
            text = kw.format_scores(scored)
        _write(text, args.out)


def cmd_ask(args) -> None:
    from .claude import ask

    summary = _load_summary(args)
    raw = Path(args.csv).read_text(encoding="utf-8-sig")
    if len(raw) > RAW_CSV_LIMIT:
        print("CSV is large; sending the summary only.", file=sys.stderr)
        raw = None
    _write(ask(args.question, summary, raw_csv=raw), args.out)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="teepublic_assistant", description="Sales analytics and Claude-powered tools for TeePublic artists.")
    sub = parser.add_subparsers(dest="command", required=True)

    def data_args(p, required=True):
        if required:
            p.add_argument("csv", help="Sales/earnings CSV from your TeePublic dashboard")
        else:
            p.add_argument("--csv", help="Optional sales CSV so Claude knows what already sells in your store")
        p.add_argument("--col", action="append", metavar="FIELD=COLUMN",
                       help=f"Map a field to a CSV column if auto-detection misses it. Fields: {', '.join(sales.COLUMN_ALIASES)}")
        p.add_argument("--top", type=int, default=10, help="How many top designs to include (default 10)")
        p.add_argument("-o", "--out", help="Write the result to this file")

    p = sub.add_parser("report", help="Sales report from your TeePublic CSV (offline, no API key needed)")
    data_args(p)
    p.add_argument("--json", action="store_true", help="Print the full summary as JSON")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("insights", help="Claude reads your sales and writes an action plan")
    data_args(p)
    p.add_argument("--goal", help='What you are aiming for, e.g. "reach $300/month before the holidays"')
    p.set_defaults(func=cmd_insights)

    p = sub.add_parser("listing", help="Claude writes or improves a design listing (title, description, tags)")
    p.add_argument("notes", nargs="?", help="Notes about the design (text, or a path to a .txt/.md file)")
    p.add_argument("--image", help="The design image (PNG/JPG/GIF/WEBP) so Claude can see it")
    p.add_argument("--existing", help="Your current listing to improve (text or file path)")
    p.add_argument("--json", action="store_true", help="Print the listing as JSON")
    data_args(p, required=False)
    p.set_defaults(func=cmd_listing)

    p = sub.add_parser("research", help="Claude searches the web for trending niches and writes design ideas with listings")
    p.add_argument("topic", nargs="?", help='Optional focus, e.g. "Christmas", "cats", "nurses", "pickleball"')
    p.add_argument("--count", type=int, default=10, help="How many opportunities to rank (default 10)")
    p.add_argument("--language", default="English", help='Report language, e.g. "Arabic" (listings stay in English)')
    data_args(p, required=False)
    p.set_defaults(func=cmd_research)

    p = sub.add_parser("design", help="Claude creates a print-ready SVG design (typography / simple vector art)")
    p.add_argument("concept", help='What to draw, e.g. "retro sunset text: Powered by Coffee and Chaos"')
    p.add_argument("--colors", help='Palette, e.g. "mustard, burnt orange, cream"')
    p.add_argument("--shirt-color", default="black", help="Shirt color it will print on (default black)")
    p.add_argument("--png", action="store_true", help="Also export a 4500x5500 PNG (needs cairosvg)")
    p.add_argument("-o", "--out", help="SVG file to write (default design.svg)")
    p.set_defaults(func=cmd_design)

    p = sub.add_parser("keywords", help="Track keywords: result counts + Google Trends, ranked by your own measurements")
    kw_sub = p.add_subparsers(dest="kw_command", required=True)
    k = kw_sub.add_parser("init", help="Create a keywords file to fill in")
    k.add_argument("file", nargs="?", default="keywords.csv")
    k = kw_sub.add_parser("add", help="Add keywords and (optionally) the number of search results you counted")
    k.add_argument("keyword", nargs="+", help='One or more phrases, e.g. "pickleball shirt"')
    k.add_argument("--teepublic", help="Number of results when you search this on TeePublic")
    k.add_argument("--etsy", help="Number of results when you search this on Etsy")
    k.add_argument("-f", "--file", default="keywords.csv")
    k = kw_sub.add_parser("trends", help="Import Google Trends 'Interest over time' CSV export(s)")
    k.add_argument("trends_csv", nargs="+", help="multiTimeline.csv file(s) downloaded from trends.google.com")
    k.add_argument("-f", "--file", default="keywords.csv")
    k = kw_sub.add_parser("score", help="Rank keywords by demand, growth and competition")
    k.add_argument("-f", "--file", default="keywords.csv")
    k.add_argument("--json", action="store_true")
    k.add_argument("-o", "--out")
    p.set_defaults(func=cmd_keywords)

    p = sub.add_parser("ask", help="Ask Claude a question about your sales data")
    data_args(p)
    p.add_argument("question")
    p.set_defaults(func=cmd_ask)

    args = parser.parse_args(argv)
    args.func(args)
