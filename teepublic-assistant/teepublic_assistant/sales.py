"""Load and summarize TeePublic sales/earnings data from a CSV file.

TeePublic has no public API for designers, so the data comes from your
designer dashboard's earnings/sales history, saved as a CSV (export it, or copy
the table into a spreadsheet and save as CSV). Column names vary, so columns
are matched against a list of aliases and can be overridden with --col.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

# Logical field -> header names we expect to see (compared case-insensitively,
# ignoring punctuation and spacing).
COLUMN_ALIASES: dict[str, list[str]] = {
    "date": ["date", "sale date", "order date", "date sold", "purchase date", "created at", "created"],
    "design": ["design", "design title", "design name", "title", "artwork", "design id"],
    "product": ["product", "product type", "product name", "item", "item type", "garment"],
    "price": ["price", "sale price", "retail price", "item price", "amount", "total"],
    "earnings": ["earnings", "your earnings", "royalty", "royalties", "commission", "payout", "net", "profit"],
    "quantity": ["quantity", "qty", "units", "count"],
    "status": ["status", "state", "transaction type", "refunded", "refund"],
    "sale_type": ["sale type", "pricing", "price type", "promo", "promotion", "discount"],
    "source": ["source", "referral", "channel", "store", "sale source", "traffic source"],
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
    design: str
    product: str
    price: float
    earnings: float
    quantity: int
    refunded: bool
    sale_type: str
    source: str


def resolve_columns(headers: list[str], overrides: dict[str, str] | None = None) -> dict[str, str]:
    """Map logical field names to the actual CSV headers."""
    overrides = overrides or {}
    by_norm = {_norm(h): h for h in headers}
    mapping: dict[str, str] = {}
    for logical, aliases in COLUMN_ALIASES.items():
        if logical in overrides:
            wanted = overrides[logical]
            if _norm(wanted) not in by_norm:
                raise ValueError(f"--col {logical}={wanted!r}: no such column. Columns are: {', '.join(headers)}")
            mapping[logical] = by_norm[_norm(wanted)]
            continue
        for alias in aliases:
            if _norm(alias) in by_norm and by_norm[_norm(alias)] not in mapping.values():
                mapping[logical] = by_norm[_norm(alias)]
                break
    if "design" not in mapping:
        raise ValueError(
            f"Could not find a design/title column. Columns are: {', '.join(headers)}. Use --col design=<column name>."
        )
    if "price" not in mapping and "earnings" not in mapping:
        raise ValueError(
            "Could not find a price or earnings column. Columns are: "
            f"{', '.join(headers)}. Use --col earnings=<column> (or --col price=<column>)."
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
            design = get(row, "design")
            if not design:
                continue
            price = parse_money(get(row, "price"))
            earnings = parse_money(get(row, "earnings")) if "earnings" in cols else price
            if "price" not in cols:
                price = 0.0
            qty_text = get(row, "quantity")
            try:
                quantity = int(float(qty_text)) if qty_text else 1
            except ValueError:
                quantity = 1
            status = get(row, "status").lower()
            refunded = "refund" in status or "cancel" in status or status in {"yes", "true"} or earnings < 0
            sales.append(
                Sale(
                    when=parse_date(get(row, "date")),
                    design=design,
                    product=get(row, "product") or "Unknown",
                    price=price,
                    earnings=earnings,
                    quantity=max(quantity, 1),
                    refunded=refunded,
                    sale_type=get(row, "sale_type"),
                    source=get(row, "source"),
                )
            )
    return sales


@dataclass
class Bucket:
    name: str
    orders: int = 0
    units: int = 0
    gross: float = 0.0
    earnings: float = 0.0
    refunds: int = 0
    first_sale: date | None = None
    last_sale: date | None = None
    products: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    monthly: dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def add(self, s: Sale) -> None:
        if s.refunded:
            self.refunds += 1
        else:
            self.orders += 1
            self.units += s.quantity
            self.gross += s.price
        self.earnings += s.earnings
        self.products[s.product] += s.earnings
        if s.when:
            self.monthly[s.when.strftime("%Y-%m")] += s.earnings
            self.first_sale = min(self.first_sale or s.when, s.when)
            self.last_sale = max(self.last_sale or s.when, s.when)


def _counts(sales: list[Sale], attr: str) -> dict[str, dict]:
    out: dict[str, dict] = defaultdict(lambda: {"orders": 0, "earnings": 0.0})
    for s in sales:
        key = getattr(s, attr)
        if key:
            out[key]["orders"] += 0 if s.refunded else 1
            out[key]["earnings"] = round(out[key]["earnings"] + s.earnings, 2)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["earnings"]))


def summarize(sales: list[Sale], top_n: int = 10) -> dict:
    """Build a JSON-serializable summary of the sales."""
    designs: dict[str, Bucket] = {}
    products: dict[str, Bucket] = {}
    monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"orders": 0, "earnings": 0.0})
    weekday: dict[str, float] = defaultdict(float)

    for s in sales:
        designs.setdefault(s.design, Bucket(s.design)).add(s)
        products.setdefault(s.product, Bucket(s.product)).add(s)
        if s.when:
            month = s.when.strftime("%Y-%m")
            monthly[month]["orders"] += 0 if s.refunded else 1
            monthly[month]["earnings"] += s.earnings
            weekday[s.when.strftime("%A")] += s.earnings

    total_earnings = sum(d.earnings for d in designs.values())
    total_orders = sum(d.orders for d in designs.values())
    ranked = sorted(designs.values(), key=lambda d: d.earnings, reverse=True)
    dates = [s.when for s in sales if s.when]
    period_end = max(dates) if dates else None

    def design_row(d: Bucket) -> dict:
        top_products = sorted(d.products.items(), key=lambda kv: -kv[1])
        return {
            "design": d.name,
            "orders": d.orders,
            "units": d.units,
            "earnings": round(d.earnings, 2),
            "earnings_per_order": round(d.earnings / d.orders, 2) if d.orders else 0.0,
            "share_of_earnings": round(d.earnings / total_earnings, 4) if total_earnings else 0.0,
            "best_products": [p for p, _ in top_products[:3]],
            "product_types_sold": len(d.products),
            "refunds": d.refunds,
            "first_sale": d.first_sale.isoformat() if d.first_sale else None,
            "last_sale": d.last_sale.isoformat() if d.last_sale else None,
            "days_since_last_sale": (period_end - d.last_sale).days if period_end and d.last_sale else None,
        }

    # Designs earning more or less in the last 3 months than the 3 before.
    months_sorted = sorted(monthly)
    trending: list[dict] = []
    if len(months_sorted) >= 6:
        recent, prior = months_sorted[-3:], months_sorted[-6:-3]
        for d in ranked:
            r = sum(d.monthly.get(m, 0.0) for m in recent)
            b = sum(d.monthly.get(m, 0.0) for m in prior)
            if b > 0 or r > 0:
                trending.append({"design": d.name, "prior_3_months": round(b, 2), "last_3_months": round(r, 2), "change": round(r - b, 2)})
        trending.sort(key=lambda t: t["change"])

    top_share = sum(d.earnings for d in ranked[:3]) / total_earnings if total_earnings else 0.0

    return {
        "period": {
            "start": min(dates).isoformat() if dates else None,
            "end": period_end.isoformat() if period_end else None,
        },
        "totals": {
            "transactions": len(sales),
            "orders": total_orders,
            "units": sum(d.units for d in designs.values()),
            "earnings": round(total_earnings, 2),
            "earnings_per_order": round(total_earnings / total_orders, 2) if total_orders else 0.0,
            "refunds": sum(d.refunds for d in designs.values()),
            "designs_with_sales": len(designs),
            "top_3_share_of_earnings": round(top_share, 4),
        },
        "by_product_type": [
            {"product": p.name, "orders": p.orders, "earnings": round(p.earnings, 2),
             "share_of_earnings": round(p.earnings / total_earnings, 4) if total_earnings else 0.0}
            for p in sorted(products.values(), key=lambda p: -p.earnings)
        ],
        "monthly": [
            {"month": m, "orders": int(v["orders"]), "earnings": round(v["earnings"], 2)}
            for m, v in sorted(monthly.items())
        ],
        "earnings_by_weekday": {d: round(v, 2) for d, v in sorted(weekday.items(), key=lambda kv: -kv[1])},
        "by_sale_type": _counts(sales, "sale_type"),
        "by_source": _counts(sales, "source"),
        "top_designs": [design_row(d) for d in ranked[:top_n]],
        "all_designs": [design_row(d) for d in ranked],
        "momentum": {"falling": trending[:5], "rising": list(reversed(trending[-5:]))} if trending else None,
    }


def _short(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def format_report(summary: dict) -> str:
    """Render a summary as plain text for the terminal."""
    t = summary["totals"]
    period = summary["period"]
    lines = [
        "TEEPUBLIC SALES REPORT",
        f"Period: {period['start'] or '?'} to {period['end'] or '?'}",
        "",
        f"  Earnings            ${t['earnings']:,.2f}",
        f"  Orders              {t['orders']:,}",
        f"  Earnings per order  ${t['earnings_per_order']:,.2f}",
        f"  Refunds             {t['refunds']:,}",
        f"  Designs selling     {t['designs_with_sales']:,}",
        f"  Top 3 designs       {t['top_3_share_of_earnings']:.0%} of earnings",
        "",
        "TOP DESIGNS",
    ]
    width = min(max((len(d["design"]) for d in summary["top_designs"]), default=10), 40)
    for i, d in enumerate(summary["top_designs"], 1):
        lines.append(
            f"  {i:>2}. {_short(d['design'], width):<{width}}  ${d['earnings']:>8,.2f}  {d['orders']:>4} orders  "
            f"{d['share_of_earnings']:>4.0%}  best on: {', '.join(d['best_products'][:2])}"
        )

    lines += ["", "BY PRODUCT TYPE"]
    for p in summary["by_product_type"]:
        lines.append(f"  {_short(p['product'], 24):<24} ${p['earnings']:>8,.2f}  {p['orders']:>4} orders  {p['share_of_earnings']:>4.0%}")

    if summary["monthly"]:
        lines += ["", "BY MONTH"]
        peak = max(m["earnings"] for m in summary["monthly"]) or 1
        for m in summary["monthly"]:
            lines.append(f"  {m['month']}  ${m['earnings']:>8,.2f}  {'█' * max(int(28 * m['earnings'] / peak), 0)}")

    for title, key in (("BY SALE TYPE", "by_sale_type"), ("BY SOURCE", "by_source")):
        if summary[key]:
            lines += ["", title]
            for name, v in summary[key].items():
                lines.append(f"  {_short(name, 24):<24} ${v['earnings']:>8,.2f}  {v['orders']:>4} orders")

    mom = summary.get("momentum")
    if mom:
        lines += ["", "MOMENTUM (last 3 months vs the 3 before)"]
        for t_ in mom["rising"]:
            if t_["change"] > 0:
                lines.append(f"  ▲ {_short(t_['design'], 40)}  +${t_['change']:,.2f}")
        for t_ in mom["falling"]:
            if t_["change"] < 0:
                lines.append(f"  ▼ {_short(t_['design'], 40)}  -${-t_['change']:,.2f}")

    return "\n".join(lines)
