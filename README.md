# febaggio.github.io

Personal CV and portfolio, published at **[febaggio.github.io](https://febaggio.github.io)**.

The site and the printable PDF are both generated from a single source of truth,
so the content only ever has to be written once.

## How it works

```
cv_data.yaml  ──┐
                ├── build.py (Jinja2) ──┬── index.html  + style.css   → the website
template.html ──┘                       └── federico_baggio_cv.pdf    → via WeasyPrint + pdf_cv.css
```

`template.html` is rendered twice against the same data: once as the web page
(styled by `style.css`) and once for print (styled by `pdf_cv.css`, which hides
the buttons and the scroll indicator and lays the content out for A4 paper).

## Building

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows;  source .venv/bin/activate on Linux/macOS
pip install -r requirements.txt
python build.py
```

`build.py` overwrites `index.html` and `federico_baggio_cv.pdf`. Both are
committed, because GitHub Pages serves them directly.

## Editing the CV

Change `cv_data.yaml` and re-run `python build.py`. Never edit `index.html` by
hand — it is generated output and will be overwritten.

## Files

| File | Role |
|---|---|
| `cv_data.yaml` | All CV content — the only file to edit for content changes |
| `template.html` | Jinja2 template, shared by the web and PDF output |
| `build.py` | Build script |
| `style.css` | Web styling |
| `pdf_cv.css` | Print styling for the PDF |
| `script.js` | Scroll indicator + copy-email button |
| `index.html` | **Generated** — the published page |
| `federico_baggio_cv.pdf` | **Generated** — the downloadable CV |
