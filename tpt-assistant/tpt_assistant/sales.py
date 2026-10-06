"""Load and summarize a Teachers Pay Teachers sales export (CSV).

TpT has no public seller API, so the data comes from the CSV you download in
your seller dashboard. Column names vary between TpT report types and have
changed over time, so columns are matched against a list of aliases and can be
overridden with --col on the command line.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

# Logical field -> header names seen in TpT exports (compared case-insensitively,
# ignoring punctuation and spacing).
COLUMN_ALIASES: dict[str, list[str]] = {
    "date": ["date", "sale date", "order date", "date sold", "purchase date", "transaction date"],
    "product": ["product", "product title", "product name", "title", "item", "resource", "resource title"],
    "product_id": ["product id", "item id", "resource id", "sku"],
    "price": ["price", "sale price", "list price", "item price", "amount", "gross", "gross sale"],
    "earnings": ["earnings", "your earnings", "net earnings", "net", "payout", "seller earnings", "royalty"],
    "quantity": ["quantity", "qty", "licenses", "number of licenses", "units"],
    "status": ["status", "type", "transaction type", "refunded", "refund"],
    "license": ["license", "license type", "licence"],
    "buyer_type": ["buyer type", "customer type", "purchase type"],
}

DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M", "%b %d, %Y", "%B %d, %Y", "%d/%m/%Y"]


def _norm(header: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", header.lower()).strip()


def parse_money(value: str | None) -> float:
    if value is None:
        return 0.0
    text = value.strip()
    if not text:
        return 0.0
    negative = text.startswith("-") or (text.startswith("(") and text.endswith(")"))
    digits = re.sub(r"[^0-9.]", "", text)
    if not digits or digits == ".":
        return 0.0
    amount = float(digits)
    return -amount if negative else amount


def parse_date(value: str | None) -> date | None:
    if not value or not value.strip():
        return None
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


@dataclass
class Sale:
    when: date | None
    product: str
    product_id: str
    price: float
    earnings: float
    quantity: int
    refunded: bool
    license: str
    buyer_type: str


def resolve_columns(headers: list[str], overrides: dict[str, str] | None = None) -> dict[str, str]:
    """Map logical field names to the actual CSV headers."""
    overrides = overrides or {}
    by_norm = {_norm(h): h for h in headers}
    mapping: dict[str, str] = {}
    for logical, aliases in COLUMN_ALIASES.items():
        if logical in overrides:
            wanted = overrides[logical]
            if wanted not in headers and _norm(wanted) not in by_norm:
                raise ValueError(f"--col {logical}={wanted!r}: no such column. Columns are: {', '.join(headers)}")
            mapping[logical] = by_norm.get(_norm(wanted), wanted)
            continue
        for alias in aliases:
            if _norm(alias) in by_norm:
                mapping[logical] = by_norm[_norm(alias)]
                break
    if "product" not in mapping:
        raise ValueError(
            "Could not find a product/title column. Columns are: "
            f"{', '.join(headers)}. Use --col product=<column name>."
        )
    if "price" not in mapping and "earnings" not in mapping:
        raise ValueError(
            "Could not find a price or earnings column. Columns are: "
            f"{', '.join(headers)}. Use --col price=<column> or --col earnings=<column>."
        )
    return mapping


def load_sales(path: str | Path, overrides: dict[str, str] | None = None) -> list[Sale]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header row")
        cols = resolve_columns(list(reader.fieldnames), overrides)

        def get(row: dict[str, str], key: str) -> str:
            return (row.get(cols[key]) or "").strip() if key in cols else ""

        sales: list[Sale] = []
        for row in reader:
            product = get(row, "product")
            if not product:
                continue
            price = parse_money(get(row, "price"))
            earnings = parse_money(get(row, "earnings")) if "earnings" in cols else price
            if "price" not in cols:
                price = earnings
            qty_text = get(row, "quantity")
            try:
                quantity = int(float(qty_text)) if qty_text else 1
            except ValueError:
                quantity = 1
            status = get(row, "status").lower()
            refunded = "refund" in status or status in {"yes", "true", "1"} or earnings < 0
            sales.append(
                Sale(
                    when=parse_date(get(row, "date")),
                    product=product,
                    product_id=get(row, "product_id"),
                    price=price,
                    earnings=earnings,
                    quantity=max(quantity, 1),
                    refunded=refunded,
                    license=get(row, "license"),
                    buyer_type=get(row, "buyer_type"),
                )
            )
    return sales


@dataclass
class ProductStats:
    product: str
    orders: int = 0
    units: int = 0
    gross: float = 0.0
    earnings: float = 0.0
    refunds: int = 0
    first_sale: date | None = None
    last_sale: date | None = None
    monthly_earnings: dict[str, float] = field(default_factory=lambda: defaultdict(float))


def summarize(sales: list[Sale], top_n: int = 10) -> dict:
    """Build a JSON-serializable summary of the sales."""
    products: dict[str, ProductStats] = {}
    monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"orders": 0, "earnings": 0.0, "gross": 0.0})
    weekday: dict[str, float] = defaultdict(float)
    licenses: dict[str, int] = defaultdict(int)
    buyer_types: dict[str, int] = defaultdict(int)

    for s in sales:
        p = products.setdefault(s.product, ProductStats(product=s.product))
        if s.refunded:
            p.refunds += 1
        else:
            p.orders += 1
            p.units += s.quantity
            p.gross += s.price
        p.earnings += s.earnings
        if s.when:
            month = s.when.strftime("%Y-%m")
            p.monthly_earnings[month] += s.earnings
            p.first_sale = min(p.first_sale or s.when, s.when)
            p.last_sale = max(p.last_sale or s.when, s.when)
            if not s.refunded:
                monthly[month]["orders"] += 1
                monthly[month]["gross"] += s.price
            monthly[month]["earnings"] += s.earnings
            weekday[s.when.strftime("%A")] += s.earnings
        if s.license:
            licenses[s.license] += 1
        if s.buyer_type:
            buyer_types[s.buyer_type] += 1

    total_earnings = sum(p.earnings for p in products.values())
    total_gross = sum(p.gross for p in products.values())
    total_orders = sum(p.orders for p in products.values())
    ranked = sorted(products.values(), key=lambda p: p.earnings, reverse=True)

    dates = [s.when for s in sales if s.when]
    period_end = max(dates) if dates else None

    def product_row(p: ProductStats) -> dict:
        return {
            "product": p.product,
            "orders": p.orders,
            "units": p.units,
            "gross": round(p.gross, 2),
            "earnings": round(p.earnings, 2),
            "avg_price": round(p.gross / p.orders, 2) if p.orders else 0.0,
            "share_of_earnings": round(p.earnings / total_earnings, 4) if total_earnings else 0.0,
            "refunds": p.refunds,
            "first_sale": p.first_sale.isoformat() if p.first_sale else None,
            "last_sale": p.last_sale.isoformat() if p.last_sale else None,
            "days_since_last_sale": (period_end - p.last_sale).days if period_end and p.last_sale else None,
        }

    # Products whose last 3 months earn less than the 3 months before (momentum check).
    months_sorted = sorted(monthly)
    trending: list[dict] = []
    if len(months_sorted) >= 6:
        recent, prior = months_sorted[-3:], months_sorted[-6:-3]
        for p in ranked:
            r = sum(p.monthly_earnings.get(m, 0.0) for m in recent)
            b = sum(p.monthly_earnings.get(m, 0.0) for m in prior)
            if b > 0 or r > 0:
                trending.append({"product": p.product, "prior_3_months": round(b, 2), "last_3_months": round(r, 2), "change": round(r - b, 2)})
        trending.sort(key=lambda t: t["change"])

    top_share = sum(p.earnings for p in ranked[:3]) / total_earnings if total_earnings else 0.0

    return {
        "period": {
            "start": min(dates).isoformat() if dates else None,
            "end": period_end.isoformat() if period_end else None,
        },
        "totals": {
            "transactions": len(sales),
            "orders": total_orders,
            "units": sum(p.units for p in products.values()),
            "gross": round(total_gross, 2),
            "earnings": round(total_earnings, 2),
            "avg_order_value": round(total_gross / total_orders, 2) if total_orders else 0.0,
            "refunds": sum(p.refunds for p in products.values()),
            "products_with_sales": len(products),
            "top_3_share_of_earnings": round(top_share, 4),
        },
        "monthly": [
            {"month": m, "orders": int(v["orders"]), "gross": round(v["gross"], 2), "earnings": round(v["earnings"], 2)}
            for m, v in sorted(monthly.items())
        ],
        "earnings_by_weekday": {d: round(v, 2) for d, v in sorted(weekday.items(), key=lambda kv: -kv[1])},
        "licenses": dict(licenses),
        "buyer_types": dict(buyer_types),
        "top_products": [product_row(p) for p in ranked[:top_n]],
        "all_products": [product_row(p) for p in ranked],
        "momentum": {"falling": trending[:5], "rising": list(reversed(trending[-5:]))} if trending else None,
    }


def format_report(summary: dict) -> str:
    """Render a summary as plain text for the terminal."""
    t = summary["totals"]
    period = summary["period"]
    lines = [
        "TpT SALES REPORT",
        f"Period: {period['start'] or '?'} to {period['end'] or '?'}",
        "",
        f"  Earnings          ${t['earnings']:,.2f}",
        f"  Gross sales       ${t['gross']:,.2f}",
        f"  Orders            {t['orders']:,}",
        f"  Avg order value   ${t['avg_order_value']:,.2f}",
        f"  Refunds           {t['refunds']:,}",
        f"  Products selling  {t['products_with_sales']:,}",
        f"  Top 3 products    {t['top_3_share_of_earnings']:.0%} of earnings",
        "",
        "TOP PRODUCTS",
    ]
    width = min(max((len(p["product"]) for p in summary["top_products"]), default=10), 50)
    for i, p in enumerate(summary["top_products"], 1):
        name = p["product"] if len(p["product"]) <= width else p["product"][: width - 1] + "…"
        lines.append(f"  {i:>2}. {name:<{width}}  ${p['earnings']:>9,.2f}  {p['orders']:>4} orders  {p['share_of_earnings']:>5.0%}")

    if summary["monthly"]:
        lines += ["", "BY MONTH"]
        peak = max(m["earnings"] for m in summary["monthly"]) or 1
        for m in summary["monthly"]:
            bar = "█" * max(int(28 * m["earnings"] / peak), 0)
            lines.append(f"  {m['month']}  ${m['earnings']:>9,.2f}  {bar}")

    if summary["earnings_by_weekday"]:
        lines += ["", "BEST DAYS"]
        for d, v in list(summary["earnings_by_weekday"].items())[:3]:
            lines.append(f"  {d:<10} ${v:,.2f}")

    mom = summary.get("momentum")
    if mom:
        lines += ["", "MOMENTUM (last 3 months vs the 3 before)"]
        for t_ in mom["rising"]:
            if t_["change"] > 0:
                lines.append(f"  ▲ {t_['product'][:50]}  +${t_['change']:,.2f}")
        for t_ in mom["falling"]:
            if t_["change"] < 0:
                lines.append(f"  ▼ {t_['product'][:50]}  -${-t_['change']:,.2f}")

    return "\n".join(lines)
