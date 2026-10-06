# TeePublic Assistant

Sales analytics and Claude-powered tools for artists selling on **TeePublic**.

- **`report`**: turns your TeePublic sales data into a report: earnings, top designs, which product types earn most, month-by-month trend, full-price vs. sale earnings, marketplace vs. your own store link, and which designs are rising or slipping. Runs offline and doesn't need an API key.
- **`insights`**: Claude reads your sales summary and writes an action plan covering designs and niches to double down on, product mix, what to fix, 5 new design ideas, and a 30-day checklist timed to upcoming holidays and gift seasons.
- **`listing`**: Claude **looks at your design image** and writes the listing: title, description, main tag, tags, target buyers, best product types, shirt colors, and variation ideas. It also flags anything that looks like a trademark or character.
- **`research`**: Claude **searches the web** for what's trending and selling right now (niches, upcoming holidays, competition) and returns ranked opportunities, each with design concepts and a ready-to-use listing. Add `--csv` to build on your own best sellers, or `--language Arabic` for the report language.
- **`design`**: Claude draws a print-ready **SVG** design (typography or simple vector art, 4500×5500, transparent background). Add `--png` to export a PNG (needs `pip install cairosvg`).
- **`ask`**: ask Claude any question about your sales data.
- **`keywords`**: rank design ideas by **numbers you measured yourself**. You record how many results a phrase gets on TeePublic/Etsy (competition) and import Google Trends exports (demand). The tool scores each phrase and flags opportunities, rising and falling phrases, crowded phrases, and seasonal phrases to upload now. Runs offline.

A full trend research report (in Arabic, October 2026) is in [`research/trends-2026-10-ar.md`](research/trends-2026-10-ar.md). A step-by-step guide to the keyword tracker (in Arabic) is in [`research/keywords-guide-ar.md`](research/keywords-guide-ar.md).

> **Important: AI art and your TeePublic tier.** TeePublic sorts artists into *Artisan* (shown in search, higher royalties) and *Apprentice* (not shown in search, half the royalties). Generic, clip-art or unedited AI-generated designs can put an account in Apprentice. Use Claude for research, ideas, slogans and listings. Treat `design` output as a starting point that you edit and make your own; don't mass-upload it as is.

> **Why a CSV?** TeePublic has no public API for designers, and automating logins or scraping your account would break TeePublic's Terms of Service. This tool uses sales data you save yourself, so your account is never touched.

## Setup

```bash
cd teepublic-assistant
pip install -r requirements.txt
pip install pillow                    # optional: shrinks big design files for `listing --image`
pip install cairosvg                  # optional: PNG export for `design --png`
export ANTHROPIC_API_KEY=sk-ant-...   # needed for every command except report
```

You can get an API key at https://console.anthropic.com.

## Get your data from TeePublic

1. Log in to TeePublic and open your **Dashboard → Earnings** (sales history).
2. If there's an export/download button, save the CSV. If not, select the sales table, paste it into Google Sheets or Excel, and use **File → Download → CSV**.

The tool auto-detects common column names (Date, Design, Product, Earnings/Royalty, Sale Type, Source, Status…). If your file uses different names, map them yourself:

```bash
python -m teepublic_assistant report sales.csv --col design="Artwork Title" --col earnings="Commission"
```

Fields: `date design product price earnings quantity status sale_type source`. Only a design column and an earnings (or price) column are required. The others make the report richer.

## Usage

Try everything on the included sample data first (it's made-up data):

```bash
# Sales report (offline)
python -m teepublic_assistant report sample_data/sample_sales.csv
python -m teepublic_assistant report sample_data/sample_sales.csv --json -o summary.json

# Claude action plan
python -m teepublic_assistant insights sample_data/sample_sales.csv --goal "reach $300/month before the holidays" -o plan.md

# Listing from your design image (+ optional notes, + your sales so it knows what sells)
python -m teepublic_assistant listing --image my_design.png "retro cat, 80s sunset" \
    --csv sample_data/sample_sales.csv -o listing.md

# Improve an existing listing
python -m teepublic_assistant listing --image my_design.png --existing current_listing.txt

# Live trend research (web search) and a design from one of the ideas
python -m teepublic_assistant research "Christmas" --csv sample_data/sample_sales.csv -o christmas.md
python -m teepublic_assistant design "retro sunset text: Powered by Coffee and Chaos" --shirt-color black --png -o coffee.svg

# Keyword tracker: your own competition counts + Google Trends exports
python -m teepublic_assistant keywords init                                   # creates keywords.csv
python -m teepublic_assistant keywords add "mahjong shirt" --teepublic 640    # results you counted on TeePublic
python -m teepublic_assistant keywords trends multiTimeline.csv               # Trends "Interest over time" download
python -m teepublic_assistant keywords score                                  # ranked table

# Ask anything
python -m teepublic_assistant ask sample_data/sample_sales.csv "Which designs should I put on hoodies before winter?"
```

Add `-o FILE` to any command to save the output.

## Tests

```bash
python -m unittest discover -s tests
```

## Notes

- Claude features use the `claude-opus-5-5` model (set in `teepublic_assistant/claude.py`) with server-side refusal fallbacks turned on.
- Listings aim for a title of 60 characters or fewer and at most 15 tags (`TITLE_LIMIT` / `MAX_TAGS` in `claude.py`). Check these limits against TeePublic's current upload form and adjust them if needed.
- `research` uses Claude's web search tool, which is billed per search on top of tokens (capped at 15 searches per run). Its report links its sources so you can check them.
- `keywords`: in Google Trends, use **Past 2 years** so growth vs. last year can be computed. Trends values are relative *within one export*, so keep one fixed anchor phrase in every comparison. The score (demand × √growth ÷ log competition) and the verdict thresholds are rules of thumb for ranking, not sales predictions. `sample_data/sample_google_trends.csv` is made-up data in the export format.
- `design` SVGs use common fonts with fallbacks. For the most reliable print, open the SVG in Inkscape/Illustrator, convert text to paths, then export the PNG.
- `insights` sends Claude only a **summary** of your sales. `ask` also sends the raw CSV when it is under about 200 KB. If your file has customer names or addresses, delete those columns first.
- Claude's suggestions are a starting point. Check tags and IP warnings before you upload. TeePublic removes designs that infringe trademarks or copyrights.
