"""Keyword tracker: rank design ideas by numbers you measured yourself.

You keep a keywords CSV with one row per search phrase. Fill in the number of
search results on TeePublic / Etsy (competition) by hand, and import Google
Trends CSV exports (demand) with `keywords trends`. `keywords score` then ranks
the phrases by demand and growth against competition.
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

FIELDS = [
    "keyword",
    "teepublic_results",   # number of results when you search TeePublic
    "etsy_results",        # number of results when you search Etsy
    "trend_recent",        # Google Trends: average of the last 3 months (0-100)
    "trend_year_ago",      # Google Trends: same 3 months one year earlier (0-100)
    "trend_growth",        # trend_recent / trend_year_ago
    "peak_month",          # month when interest is usually highest
    "trends_file",         # which Google Trends export the numbers came from
    "checked_on",          # date you measured
    "notes",
]

# Starter phrases so the file isn't empty; edit or delete them.
EXAMPLE_ROWS = [{"keyword": "pickleball shirt"}, {"keyword": "mahjong shirt"}, {"keyword": "nurse christmas shirt"}]

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def _num(value: str | None) -> float | None:
    """Parse '12,345', '1.2k', '<1' and similar; None when empty."""
    if value is None:
        return None
    text = value.strip().lower().replace(",", "")
    if not text:
        return None
    if text.startswith("<"):
        return 0.5
    mult = 1.0
    if text.endswith("k"):
        mult, text = 1_000.0, text[:-1]
    elif text.endswith("m"):
        mult, text = 1_000_000.0, text[:-1]
    text = re.sub(r"[^0-9.]", "", text)
    if not text or text == ".":
        return None
    return float(text) * mult


def _fmt(value: float | None, digits: int = 1) -> str:
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.{digits}f}"


# --- The keywords file -------------------------------------------------------

def init_file(path: str | Path) -> None:
    path = Path(path)
    if path.exists():
        raise SystemExit(f"{path} already exists; not overwriting it.")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in EXAMPLE_ROWS:
            w.writerow(row)


def read_file(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = {"keyword"} - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"{path} needs a 'keyword' column. Create one with: keywords init {path}")
        rows = []
        for row in reader:
            if (row.get("keyword") or "").strip():
                rows.append({k: (row.get(k) or "").strip() for k in FIELDS} | {"keyword": row["keyword"].strip()})
        return rows


def write_file(path: str | Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def add_keywords(path: str | Path, keywords: list[str], teepublic: str | None = None, etsy: str | None = None) -> list[str]:
    rows = read_file(path)
    by_kw = {r["keyword"].lower(): r for r in rows}
    changed = []
    for kw in keywords:
        row = by_kw.get(kw.lower())
        if row is None:
            row = {k: "" for k in FIELDS} | {"keyword": kw}
            rows.append(row)
            by_kw[kw.lower()] = row
        if teepublic is not None:
            row["teepublic_results"] = teepublic
        if etsy is not None:
            row["etsy_results"] = etsy
        if teepublic is not None or etsy is not None:
            row["checked_on"] = date.today().isoformat()
        changed.append(kw)
    write_file(path, rows)
    return changed


# --- Google Trends import ----------------------------------------------------

@dataclass
class TrendSeries:
    keyword: str
    points: list[tuple[date, float]]

    def window_avg(self, start: date, end: date) -> float | None:
        vals = [v for d, v in self.points if start <= d <= end]
        return sum(vals) / len(vals) if vals else None

    def peak_month(self) -> str | None:
        by_month: dict[int, list[float]] = {}
        for d, v in self.points:
            by_month.setdefault(d.month, []).append(v)
        if not by_month:
            return None
        best = max(by_month, key=lambda m: sum(by_month[m]) / len(by_month[m]))
        return MONTHS[best - 1]


def _parse_trend_date(text: str) -> date | None:
    text = text.strip()
    for candidate in (text, text[:10]):
        try:
            return date.fromisoformat(candidate)
        except ValueError:
            pass
    m = re.match(r"^(\d{4})-(\d{2})$", text)  # monthly exports: 2025-10
    if m:
        return date(int(m.group(1)), int(m.group(2)), 1)
    # Other layouts ("Oct 5, 2025", "10/05/2025", "2025-10-05 - 2025-10-11" ranges)
    from .sales import parse_date
    return parse_date(text.split(" - ")[0]) or parse_date(text.split("–")[0])


def parse_trends_csv(path: str | Path) -> list[TrendSeries]:
    """Read a Google Trends 'Interest over time' CSV export (multiTimeline.csv).

    The file starts with a 'Category: …' line and a blank line before the
    header row (Week/Month/Day/Time, then one column per search term like
    'pickleball shirt: (United States)').
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        lines = list(csv.reader(f))
    header_at = None
    for i, row in enumerate(lines):
        if row and row[0].strip().lower() in {"week", "month", "day", "time", "date"} and len(row) >= 2:
            header_at = i
            break
    if header_at is None:
        raise SystemExit(
            f"{path} doesn't look like a Google Trends 'Interest over time' export "
            "(expected a header row starting with Week, Month, Day or Time)."
        )
    names = [re.sub(r":\s*\(.*\)\s*$", "", h).strip() for h in lines[header_at][1:]]
    series = [TrendSeries(n, []) for n in names]
    for row in lines[header_at + 1:]:
        if not row or not row[0].strip():
            continue
        when = _parse_trend_date(row[0])
        if when is None:
            continue
        for s, cell in zip(series, row[1:]):
            v = _num(cell)
            if v is not None:
                s.points.append((when, v))
    return [s for s in series if s.points]


def import_trends(keywords_path: str | Path, trends_path: str | Path) -> list[dict]:
    """Merge a Google Trends export into the keywords file; returns the updated rows."""
    series = parse_trends_csv(trends_path)
    if not series:
        raise SystemExit(f"No data found in {trends_path}")
    rows = read_file(keywords_path)
    by_kw = {r["keyword"].lower(): r for r in rows}
    latest = max(d for s in series for d, _ in s.points)
    # "Recent" = the last ~3 months of the export; "year ago" = the same window 52 weeks earlier.
    recent_start = date.fromordinal(latest.toordinal() - 90)
    year_ago_end = date.fromordinal(latest.toordinal() - 364)
    year_ago_start = date.fromordinal(recent_start.toordinal() - 364)
    updated = []
    for s in series:
        row = by_kw.get(s.keyword.lower())
        if row is None:
            row = {k: "" for k in FIELDS} | {"keyword": s.keyword}
            rows.append(row)
            by_kw[s.keyword.lower()] = row
        recent = s.window_avg(recent_start, latest)
        ago = s.window_avg(year_ago_start, year_ago_end)
        row["trend_recent"] = _fmt(recent)
        row["trend_year_ago"] = _fmt(ago)
        row["trend_growth"] = _fmt(recent / ago, 2) if recent is not None and ago else ""
        row["peak_month"] = s.peak_month() or ""
        row["trends_file"] = Path(trends_path).name
        row["checked_on"] = date.today().isoformat()
        updated.append(row)
    write_file(keywords_path, rows)
    return updated


# --- Scoring -----------------------------------------------------------------

def months_until(month_name: str, today: date) -> int | None:
    if month_name not in MONTHS:
        return None
    return (MONTHS.index(month_name) + 1 - today.month) % 12


def score_rows(rows: list[dict], today: date | None = None) -> list[dict]:
    """Rank keywords: demand x growth / competition.

    - demand: trend_recent (Google Trends 0-100). Only comparable between keywords
      from the same Trends export, so keep a fixed "anchor" keyword in every export.
    - growth: trend_recent / trend_year_ago, capped to 0.25-4 so one spike can't dominate.
    - competition: TeePublic results (or Etsy when TeePublic is missing), on a log scale.
    """
    today = today or date.today()
    scored = []
    for r in rows:
        demand = _num(r.get("trend_recent"))
        growth = _num(r.get("trend_growth"))
        tp = _num(r.get("teepublic_results"))
        etsy = _num(r.get("etsy_results"))
        competition = tp if tp is not None else etsy
        missing = []
        if demand is None:
            missing.append("Google Trends")
        if competition is None:
            missing.append("result count")
        score = None
        if not missing:
            g = min(max(growth if growth else 1.0, 0.25), 4.0)
            score = round(demand * math.sqrt(g) / math.log10(competition + 10) * 10, 1)
        to_peak = months_until(r.get("peak_month", ""), today)
        if score is None:
            verdict = "needs " + " + ".join(missing)
        elif to_peak is not None and 1 <= to_peak <= 3 and not (growth and growth <= 0.6):
            # Seasonal: demand looks low now but peaks soon; designs need weeks to get indexed.
            verdict = f"seasonal: peaks in {r['peak_month']}, upload now"
        elif competition is not None and competition < 2_000 and (demand or 0) >= 10:
            verdict = "opportunity: demand with little competition"
        elif growth and growth >= 1.5:
            verdict = "rising"
        elif growth and growth <= 0.6:
            verdict = "falling"
        elif competition is not None and competition > 100_000:
            verdict = "crowded: narrow it down"
        else:
            verdict = "ok"
        scored.append(r | {"score": score, "verdict": verdict, "_competition": competition})
    scored.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0)))
    return scored


def format_scores(scored: list[dict]) -> str:
    width = min(max((len(r["keyword"]) for r in scored), default=10), 34)
    lines = [
        "KEYWORD RANKING (your own measurements)",
        "",
        f"  {'#':>2}  {'keyword':<{width}}  {'score':>6}  {'trend':>5}  {'growth':>6}  {'results':>9}  {'peak':<9}  verdict",
    ]
    for i, r in enumerate(scored, 1):
        kw = r["keyword"] if len(r["keyword"]) <= width else r["keyword"][: width - 1] + "…"
        comp = r["_competition"]
        lines.append(
            f"  {i:>2}  {kw:<{width}}  {_fmt(r['score']) or '-':>6}  {r['trend_recent'] or '-':>5}  "
            f"{(r['trend_growth'] + 'x') if r['trend_growth'] else '-':>6}  "
            f"{f'{comp:,.0f}' if comp is not None else '-':>9}  {(r['peak_month'] or '-')[:9]:<9}  {r['verdict']}"
        )
    files = sorted({r["trends_file"] for r in scored if r.get("trends_file")})
    if len(files) > 1:
        lines += ["", f"Note: trend numbers come from {len(files)} different Google Trends exports. "
                      "Trend values are only comparable within the same export."]
    return "\n".join(lines)
