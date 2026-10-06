"""Claude-powered helpers: sales insights, listing writer, and Q&A over your data."""

from __future__ import annotations

import json

import anthropic

MODEL = "claude-opus-5-5"

SELLER_CONTEXT = (
    "You are an experienced Teachers Pay Teachers (TpT) seller coach. You know how TpT "
    "search works (titles, descriptions, grade/subject/resource-type filters, tags), how "
    "teachers shop (by standard, grade, season and immediate classroom need), and the "
    "seasonal rhythm of the US school year (back to school in Jul-Sep, holidays, test prep "
    "in spring, end-of-year in May-Jun, and site-wide sales). Give specific, practical advice "
    "a solo teacher-author can act on this week. Never invent numbers: when you cite a figure "
    "it must come from the data you were given."
)


def _call(prompt: str, *, schema: dict | None = None, effort: str = "high", max_tokens: int = 16000) -> str:
    """Send one request and return the text of the response.

    Uses server-side refusal fallbacks so a request declined by a safety
    classifier is retried on Anthropic's recommended fallback model.
    """
    client = anthropic.Anthropic()
    output_config: dict = {"effort": effort}
    if schema:
        output_config["format"] = {"type": "json_schema", "schema": schema}
    try:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=SELLER_CONTEXT,
            output_config=output_config,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError:
        raise SystemExit("Claude rejected the API key. Set ANTHROPIC_API_KEY (see README).")
    except anthropic.RateLimitError:
        raise SystemExit("Rate limited by the Claude API. Wait a minute and try again.")
    except anthropic.APIStatusError as e:
        raise SystemExit(f"Claude API error ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError:
        raise SystemExit("Could not reach the Claude API. Check your internet connection.")

    if response.stop_reason == "refusal":
        reason = response.stop_details.explanation if response.stop_details else "no details"
        raise SystemExit(f"Claude declined this request: {reason}")
    if response.stop_reason == "max_tokens":
        raise SystemExit("Claude's answer was cut off (max_tokens). Try a narrower request.")
    return "".join(b.text for b in response.content if b.type == "text")


# --- Sales insights --------------------------------------------------------

def sales_insights(summary: dict, goal: str | None = None) -> str:
    data = json.dumps(summary, indent=1)
    prompt = (
        "Here is a summary of my TpT store's sales export:\n\n"
        f"<sales_summary>\n{data}\n</sales_summary>\n\n"
        + (f"My goal right now: {goal}\n\n" if goal else "")
        + "Write me an action plan in Markdown with these sections:\n"
        "1. **Snapshot** - 3-4 bullets on what the numbers say (cite the figures).\n"
        "2. **Double down** - which products are carrying the store and how to get more from them "
        "(bundles, companion resources, differentiated versions, better previews).\n"
        "3. **Fix or retire** - products that are slipping or under-earning, and what to change first "
        "(title, thumbnail, price, description).\n"
        "4. **Pricing** - concrete price or bundle suggestions with reasoning.\n"
        "5. **What to make next** - 3-5 new product ideas grounded in what already sells.\n"
        "6. **Next 30 days** - a short checklist ordered by expected impact, timed to the school calendar "
        f"(the data ends on {summary['period']['end'] or 'an unknown date'}).\n"
        "Keep it tight; skip generic advice that doesn't follow from this data."
    )
    return _call(prompt, effort="high")


# --- Listing writer --------------------------------------------------------

LISTING_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Search-friendly product title, at most 80 characters."},
        "alternate_titles": {"type": "array", "items": {"type": "string"}},
        "short_description": {"type": "string", "description": "1-2 sentence hook for the top of the description."},
        "description": {"type": "string", "description": "Full product description in plain text with simple section headings and bullet points."},
        "whats_included": {"type": "array", "items": {"type": "string"}},
        "grades": {"type": "array", "items": {"type": "string"}},
        "subjects": {"type": "array", "items": {"type": "string"}},
        "resource_types": {"type": "array", "items": {"type": "string"}},
        "standards": {"type": "array", "items": {"type": "string"}, "description": "Only standards the product actually covers; empty if unknown."},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "Search keywords teachers would type."},
        "suggested_price_usd": {"type": "number"},
        "price_reasoning": {"type": "string"},
        "thumbnail_ideas": {"type": "array", "items": {"type": "string"}},
        "preview_ideas": {"type": "array", "items": {"type": "string"}},
        "seasonal_timing": {"type": "string", "description": "When this sells best and when to promote it."},
    },
    "required": [
        "title", "alternate_titles", "short_description", "description", "whats_included", "grades",
        "subjects", "resource_types", "standards", "tags", "suggested_price_usd", "price_reasoning",
        "thumbnail_ideas", "preview_ideas", "seasonal_timing",
    ],
    "additionalProperties": False,
}


def write_listing(product_notes: str, existing_listing: str | None = None, store_summary: dict | None = None) -> dict:
    parts = [
        "Write a complete TpT product listing for this resource.",
        f"<product_notes>\n{product_notes}\n</product_notes>",
    ]
    if existing_listing:
        parts.append(
            "This is the current listing. Improve it for search and conversion, keep anything accurate "
            f"that is working, and don't claim contents that aren't in the notes:\n<current_listing>\n{existing_listing}\n</current_listing>"
        )
    if store_summary:
        best = [p["product"] for p in store_summary.get("top_products", [])[:5]]
        prices = [p["avg_price"] for p in store_summary.get("top_products", []) if p["avg_price"]]
        parts.append(
            f"For context, my best sellers are: {json.dumps(best)}; their average prices are {json.dumps(prices)}. "
            "Price consistently with my store and mention companion products only if they truly fit."
        )
    parts.append(
        "Rules: the title must be 80 characters or fewer and lead with what teachers search for "
        "(topic + grade + resource type). Only list contents, standards and grade levels supported by the notes."
    )
    listing = json.loads(_call("\n\n".join(parts), schema=LISTING_SCHEMA, effort="medium"))
    if len(listing["title"]) > 80:
        listing["title_warning"] = f"Title is {len(listing['title'])} characters; TpT allows 80."
    return listing


def format_listing(listing: dict) -> str:
    def bullets(items: list) -> str:
        return "\n".join(f"- {i}" for i in items) or "- (none)"

    return "\n".join([
        f"# {listing['title']}  ({len(listing['title'])}/80 chars)",
        *( [f"> ⚠ {listing['title_warning']}"] if listing.get("title_warning") else [] ),
        "",
        "**Other title options**",
        bullets(listing["alternate_titles"]),
        "",
        f"**Hook:** {listing['short_description']}",
        "",
        "## Description",
        listing["description"],
        "",
        "## What's included",
        bullets(listing["whats_included"]),
        "",
        f"**Grades:** {', '.join(listing['grades'])}",
        f"**Subjects:** {', '.join(listing['subjects'])}",
        f"**Resource types:** {', '.join(listing['resource_types'])}",
        f"**Standards:** {', '.join(listing['standards']) or '—'}",
        f"**Tags:** {', '.join(listing['tags'])}",
        "",
        f"**Suggested price:** ${listing['suggested_price_usd']:.2f} — {listing['price_reasoning']}",
        "",
        "## Thumbnail ideas",
        bullets(listing["thumbnail_ideas"]),
        "",
        "## Preview ideas",
        bullets(listing["preview_ideas"]),
        "",
        f"**When to promote:** {listing['seasonal_timing']}",
    ])


# --- Q&A over the data -----------------------------------------------------

def ask(question: str, summary: dict, raw_csv: str | None = None) -> str:
    parts = [f"<sales_summary>\n{json.dumps(summary, indent=1)}\n</sales_summary>"]
    if raw_csv:
        parts.append(f"<raw_sales_csv>\n{raw_csv}\n</raw_sales_csv>")
    parts.append(
        f"Question about my TpT store: {question}\n\n"
        "Answer directly using the data above. If the data can't answer it, say what's missing "
        "and which TpT report would contain it."
    )
    return _call("\n\n".join(parts), effort="medium")
