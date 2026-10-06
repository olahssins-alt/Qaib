# TpT Assistant

Sales analytics and Claude-powered tools for **Teachers Pay Teachers** sellers.

- **`report`**: turns your TpT sales CSV into a report: earnings, top products, month-by-month trend, best days, and which products are rising or slipping. Runs offline and doesn't need an API key.
- **`insights`**: Claude reads your sales summary and writes an action plan covering what to double down on, what to fix, pricing, what to make next, and a 30-day checklist timed to the school calendar.
- **`listing`**: Claude writes or improves a product listing: an SEO title (80 characters or fewer), description, grades, subjects, tags, a suggested price, and thumbnail and preview ideas.
- **`ask`**: ask Claude any question about your sales data.

> **Why a CSV?** TpT has no public API for sellers, and automating logins or scraping your account would break TpT's Terms of Service. This tool uses the sales report you download yourself from the seller dashboard, so your account is never touched.

## Setup

```bash
cd tpt-assistant
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # only needed for insights / listing / ask
```

You can get an API key at https://console.anthropic.com.

## Get your data from TpT

1. Log in to TpT and open **Dashboard → My Sales** (in some versions this is **Seller Dashboard → Sales Reports**).
2. Choose a date range. A full year works best for trends.
3. Click **Export / Download CSV**.

The tool auto-detects common column names (Date, Product Title, Sale Price, Your Earnings, Licenses, Status…). If your export uses different names, map them yourself:

```bash
python -m tpt_assistant report sales.csv --col product="Resource Name" --col earnings="Net"
```

Fields: `date product product_id price earnings quantity status license buyer_type`.

## Usage

Try everything on the included sample data first (it's made-up data):

```bash
# Sales report (offline)
python -m tpt_assistant report sample_data/sample_sales.csv
python -m tpt_assistant report sample_data/sample_sales.csv --json -o summary.json

# Claude action plan
python -m tpt_assistant insights sample_data/sample_sales.csv --goal "reach $600/month by back to school" -o plan.md

# Write a new listing from your notes (text or a file)
python -m tpt_assistant listing "32 task cards on equivalent fractions, 3rd grade, answer key, recording sheet, QR codes" \
    --csv sample_data/sample_sales.csv -o listing.md

# Improve an existing listing
python -m tpt_assistant listing notes.txt --existing current_listing.txt

# Ask anything
python -m tpt_assistant ask sample_data/sample_sales.csv "Which product should I bundle with my reading passages?"
```

Add `-o FILE` to any command to save the output.

## Tests

```bash
python -m unittest discover -s tests
```

## Notes

- Claude features use the `claude-opus-5-5` model (set in `tpt_assistant/claude.py`) with server-side refusal fallbacks turned on.
- Only the **summary** of your sales is sent to Claude for `insights`. `ask` also sends the raw CSV when it is under about 200 KB, so Claude can answer detailed questions. Buyer names and emails aren't used. If your export has them, you can delete those columns before running `ask`.
- Claude's suggestions are a starting point. Check prices, standards, and claims before you publish.
