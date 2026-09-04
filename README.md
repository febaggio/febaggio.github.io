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

Change `cv_data.yaml`, bump its `info.updated` date, and re-run
`python build.py`. Never edit `index.html` by hand — it is generated output and
will be overwritten.

The build is reproducible: the same `cv_data.yaml` always produces a
byte-identical PDF, so `git status` stays clean unless the CV actually changed.
That is what `info.updated` is for — it is the date stamped into the PDF, and
pinning it keeps the embedded fonts from carrying a fresh timestamp each run.

### Social preview image

`og-image.png` is the card shown when the site is shared. It is generated
separately, since it only changes when the name or tagline does:

```bash
python make_og_image.py
```

## Automatic builds

Pushing a change to `cv_data.yaml` (or to the template, the stylesheets or
`build.py`) triggers `.github/workflows/build.yml`, which rebuilds `index.html`
and the PDF and commits them back. So editing the YAML on GitHub directly is
enough to update the site.

The workflow only watches the input files, never the generated ones, so its own
commit cannot trigger another run. It commits only when the output actually
changed, which is what the reproducible build buys us.

Building locally still works exactly the same; just push the regenerated files
along with the sources and the workflow will find nothing to do.

## Files

| File | Role |
|---|---|
| `cv_data.yaml` | All CV content — the only file to edit for content changes |
| `template.html` | Jinja2 template, shared by the web and PDF output |
| `build.py` | Build script |
| `style.css` | Web styling |
| `pdf_cv.css` | Print styling for the PDF |
| `script.js` | Scroll indicator + copy-email button |
| `make_og_image.py` | Generates `og-image.png`, run manually |
| `index.html` | **Generated** — the published page |
| `federico_baggio_cv.pdf` | **Generated** — the downloadable CV |
| `og-image.png` | **Generated** — social link preview |
| `.github/workflows/build.yml` | Rebuilds and commits the output on push |
