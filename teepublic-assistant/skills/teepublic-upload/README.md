# teepublic-upload

A skill for Claude Cowork. Install it, then each day send: "Upload and publish this: <Upload Desk link>".

Build a day's page: `python scripts/desk/make_upload_desk.py batch.json page.html` (see `examples/batch-data-example.json` for the fields), then publish the HTML as an Artifact with the `downloads` capability.
