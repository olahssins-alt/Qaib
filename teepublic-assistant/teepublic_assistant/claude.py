"""Claude-powered helpers: sales insights, design listings, and Q&A over your data."""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-5-5"

# Listing limits we write to. Check them against TeePublic's current upload form.
TITLE_LIMIT = 60
MAX_TAGS = 15

# The API accepts images up to 5 MB; print-ready design files are often larger.
MAX_IMAGE_BYTES = 5 * 1024 * 1024
MEDIA_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp"}

SELLER_CONTEXT = (
    "You are an experienced print-on-demand coach who helps independent artists sell on "
    "TeePublic. You understand how buyers find designs (search on titles and tags, browsing "
    "by niche, fandom, hobby, profession, humor and occasion), which product types suit "
    "which kinds of art (t-shirts, hoodies, stickers, mugs, phone cases, wall art, etc.), and "
    "the seasonal rhythm of gift-buying (holidays, Mother's/Father's Day, back to school, "
    "Halloween, Black Friday/Cyber Monday) and site-wide sales. Give specific, practical advice "
    "a solo artist can act on this week. Never invent numbers: any figure you cite must come "
    "from the data you were given. Never suggest copying trademarked characters, brands, logos "
    "or other artists' work; steer toward original designs."
)


def _call(content: str | list, *, schema: dict | None = None, effort: str = "high", max_tokens: int = 16000) -> str:
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
            messages=[{"role": "user", "content": content}],
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


def image_block(path: str | Path) -> dict:
    """Build an image content block, shrinking big design files if Pillow is available."""
    path = Path(path)
    media_type = MEDIA_TYPES.get(path.suffix.lower())
    if not media_type:
        raise SystemExit(f"{path.name}: use a PNG, JPG, GIF or WEBP image.")
    data = path.read_bytes()
    if len(data) > MAX_IMAGE_BYTES:
        try:
            from PIL import Image
        except ImportError:
            raise SystemExit(
                f"{path.name} is {len(data) / 1e6:.1f} MB; Claude accepts up to 5 MB. "
                "Run `pip install pillow` so it can be shrunk automatically, or export a smaller preview."
            )
        img = Image.open(path)
        img.thumbnail((1600, 1600))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        data, media_type = buf.getvalue(), "image/png"
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64.standard_b64encode(data).decode()}}


# --- Sales insights --------------------------------------------------------

def sales_insights(summary: dict, goal: str | None = None) -> str:
    prompt = (
        "Here is a summary of my TeePublic sales data:\n\n"
        f"<sales_summary>\n{json.dumps(summary, indent=1)}\n</sales_summary>\n\n"
        + (f"My goal right now: {goal}\n\n" if goal else "")
        + "Write me an action plan in Markdown with these sections:\n"
        "1. **Snapshot** - 3-4 bullets on what the numbers say (cite the figures).\n"
        "2. **Double down** - which designs and niches are carrying the store, and how to get more from "
        "them (variations, color/wording versions, the same idea for related niches, product types to push).\n"
        "3. **Product mix** - which product types earn best for my art and which to promote or check are enabled.\n"
        "4. **Fix or retire** - designs that are slipping or never took off, and what to change first "
        "(title, tags, mockup color, default product).\n"
        "5. **What to design next** - 5 original design ideas grounded in what already sells.\n"
        "6. **Next 30 days** - a short checklist ordered by expected impact, timed to upcoming holidays and "
        f"gift seasons (the data ends on {summary['period']['end'] or 'an unknown date'}).\n"
        "Keep it tight; skip generic advice that doesn't follow from this data."
    )
    return _call(prompt, effort="high")


# --- Design listing writer -------------------------------------------------

LISTING_SCHEMA = {
    "type": "object",
    "properties": {
        "design_read": {"type": "string", "description": "One or two sentences on what the design shows and who it appeals to."},
        "title": {"type": "string", "description": "Search-friendly, short design title."},
        "alternate_titles": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "string", "description": "Short, friendly product description (2-4 sentences)."},
        "main_tag": {"type": "string", "description": "The single most important search term for this design."},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "Additional search tags, most important first."},
        "target_buyers": {"type": "array", "items": {"type": "string"}, "description": "Who buys this and for what occasion."},
        "best_product_types": {"type": "array", "items": {"type": "string"}},
        "default_product": {"type": "string", "description": "Which product to feature as the main mockup."},
        "garment_colors": {"type": "array", "items": {"type": "string"}, "description": "Shirt colors the art reads well on."},
        "variation_ideas": {"type": "array", "items": {"type": "string"}, "description": "Original spin-off designs to make next."},
        "promotion_timing": {"type": "string", "description": "When this design sells best and when to promote it."},
        "ip_warnings": {"type": "array", "items": {"type": "string"}, "description": "Anything that looks like a trademark, brand, character or copyrighted phrase. Empty if none."},
    },
    "required": [
        "design_read", "title", "alternate_titles", "description", "main_tag", "tags", "target_buyers",
        "best_product_types", "default_product", "garment_colors", "variation_ideas", "promotion_timing", "ip_warnings",
    ],
    "additionalProperties": False,
}


def write_listing(notes: str | None = None, image: str | Path | None = None, existing_listing: str | None = None,
                  store_summary: dict | None = None) -> dict:
    if not notes and not image:
        raise SystemExit("Give the design image, some notes about it, or both.")
    content: list[dict] = []
    if image:
        content.append(image_block(image))
    parts = ["Write a complete TeePublic listing for this design" + (" (image attached)." if image else ".")]
    if notes:
        parts.append(f"<design_notes>\n{notes}\n</design_notes>")
    if existing_listing:
        parts.append(
            "This is the current listing. Improve it for search and conversion and keep anything that "
            f"is working:\n<current_listing>\n{existing_listing}\n</current_listing>"
        )
    if store_summary:
        best = [d["design"] for d in store_summary.get("top_designs", [])[:5]]
        product_mix = [p["product"] for p in store_summary.get("by_product_type", [])[:5]]
        parts.append(
            f"For context, my best-selling designs are {json.dumps(best)} and my best product types are "
            f"{json.dumps(product_mix)}. Use that to judge what my buyers respond to."
        )
    parts.append(
        f"Rules: the title must be {TITLE_LIMIT} characters or fewer, give at most {MAX_TAGS} tags, and use the words buyers would search. "
        "Tags are lowercase search phrases, no '#', no duplicates of the main tag, and must never include brand or "
        "character names the design doesn't legitimately own. If the design or notes look like they use "
        "someone else's trademark or character, say so in ip_warnings."
    )
    content.append({"type": "text", "text": "\n\n".join(parts)})
    listing = json.loads(_call(content, schema=LISTING_SCHEMA, effort="medium"))
    listing["tags"] = listing["tags"][:MAX_TAGS]
    return listing


def format_listing(listing: dict) -> str:
    def bullets(items: list) -> str:
        return "\n".join(f"- {i}" for i in items) or "- (none)"

    title = listing["title"]
    lines = [f"# {title}  ({len(title)}/{TITLE_LIMIT} chars)"]
    if len(title) > TITLE_LIMIT:
        lines.append(f"> ⚠ Title is {len(title)} characters; shorten it to {TITLE_LIMIT} or fewer.")
    if listing["ip_warnings"]:
        lines += ["", "> ⚠ **Possible IP issues — check before uploading:**", *[f"> - {w}" for w in listing["ip_warnings"]]]
    lines += [
        "",
        f"_{listing['design_read']}_",
        "",
        "**Other title options**",
        bullets(listing["alternate_titles"]),
        "",
        "## Description",
        listing["description"],
        "",
        f"**Main tag:** {listing['main_tag']}",
        f"**Tags:** {', '.join(listing['tags'])}",
        "",
        "## Who buys it",
        bullets(listing["target_buyers"]),
        "",
        f"**Default product:** {listing['default_product']}",
        f"**Best product types:** {', '.join(listing['best_product_types'])}",
        f"**Shirt colors:** {', '.join(listing['garment_colors'])}",
        "",
        "## Variations to design next",
        bullets(listing["variation_ideas"]),
        "",
        f"**When to promote:** {listing['promotion_timing']}",
    ]
    return "\n".join(lines)


# --- Q&A over the data -----------------------------------------------------

def ask(question: str, summary: dict, raw_csv: str | None = None) -> str:
    parts = [f"<sales_summary>\n{json.dumps(summary, indent=1)}\n</sales_summary>"]
    if raw_csv:
        parts.append(f"<raw_sales_csv>\n{raw_csv}\n</raw_sales_csv>")
    parts.append(
        f"Question about my TeePublic store: {question}\n\n"
        "Answer directly using the data above. If the data can't answer it, say what's missing."
    )
    return _call("\n\n".join(parts), effort="medium")
