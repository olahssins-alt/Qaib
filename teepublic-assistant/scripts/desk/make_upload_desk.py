"""Build the daily Upload Desk page from a batch file.

Usage: python scripts/desk/make_upload_desk.py batch.json out.html
batch.json: {"date": "2026-10-08", "designs": [{"id", "png" (path), "title", "main_tag", "tags": [...],
             "description", "products", "colors"}]}
The page embeds the PNGs (for the Save button) and a plain JSON block (id="batch-data") with the text
fields only, which an upload agent can read cheaply. Publish the HTML with the Artifact tool and the
`downloads` capability.
"""
import base64, json, sys
from pathlib import Path

batch = json.load(open(sys.argv[1]))
base = Path(sys.argv[1]).parent
cards, plain = [], []
for d in batch["designs"]:
    png = base64.b64encode((base / d["png"]).read_bytes()).decode()
    cards.append(dict(slug=d["id"], head=d.get("heading", d["title"]), title=d["title"], main=d["main_tag"], tags=d["tags"],
                      desc=d["description"], prod=d["products"], colors=d["colors"], png=png))
    plain.append({k: d[k] for k in ("id", "title", "main_tag", "tags", "description", "products", "colors")})
tpl = (Path(__file__).parent / "upload_desk.tpl.html").read_text()
html = (tpl.replace("__BATCH_JSON__", json.dumps({"date": batch["date"], "designs": plain}).replace("</", "<\\/"))
           .replace("__BATCH_META__", json.dumps({"date": batch["date"]}))
           .replace("__DATA__", json.dumps(cards).replace("</", "<\\/")))
Path(sys.argv[2]).write_text(html)
print(f"{len(cards)} designs, {len(html)/1e6:.1f} MB")
