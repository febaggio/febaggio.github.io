import os
from datetime import datetime, timezone

import yaml
from jinja2 import Environment, FileSystemLoader

# Fixed document id: WeasyPrint would otherwise put a random one in every
# file, which alone would make the output differ between builds.
PDF_IDENTIFIER = b'febaggio-cv'


def _set_build_date(updated):
    """
    Pin every timestamp the PDF contains to the CV's own "updated" date.

    The PDF is committed to the repo, so it must be byte-for-byte
    reproducible: otherwise each build shows up as a diff even when the CV
    has not changed. The bytes that used to vary were timestamps fontTools
    writes into the subsetted fonts, and it honours SOURCE_DATE_EPOCH.

    This has to run before WeasyPrint is imported, since importing it pulls
    in the font machinery.
    """
    date = datetime.strptime(updated, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    os.environ['SOURCE_DATE_EPOCH'] = str(int(date.timestamp()))
    return date.strftime('%Y-%m-%d')


def build_cv():
    """
    Reads data from cv_data.yaml, renders it into index.html using template.html,
    and subsequently generates a PDF version of the CV.
    """
    print("[INFO] Starting CV generation process...")

    # ---------------------------------------------------------
    # 1. Load Data
    # ---------------------------------------------------------
    try:
        with open('cv_data.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        print("[INFO] Data successfully loaded from cv_data.yaml")
    except FileNotFoundError:
        print("[ERROR] File 'cv_data.yaml' not found. Please ensure it exists in the root directory.")
        return
    except yaml.YAMLError as exc:
        print(f"[ERROR] Error parsing YAML file: {exc}")
        return

    try:
        build_date = _set_build_date(data['info']['updated'])
    except (KeyError, ValueError):
        print("[ERROR] cv_data.yaml needs an info.updated date in YYYY-MM-DD form.")
        return

    # Imported only now: it must not load the font machinery before
    # _set_build_date has put SOURCE_DATE_EPOCH in the environment.
    from weasyprint import HTML, CSS

    # ---------------------------------------------------------
    # 2. Render HTML Template
    # ---------------------------------------------------------
    try:
        # Set up the Jinja2 environment to load templates from the current directory
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')
        
        # Render the template with the data loaded from YAML.
        # build_date feeds the dcterms meta tags the PDF takes its dates from.
        html_output = template.render(build_date=build_date, **data)
    except Exception as e:
        print(f"[ERROR] Template rendering failed: {e}")
        return

    # ---------------------------------------------------------
    # 3. Write Static HTML Site
    # ---------------------------------------------------------
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_output)
        print("[INFO] Website updated: index.html")
    except IOError as e:
        print(f"[ERROR] Could not write index.html: {e}")

    # ---------------------------------------------------------
    # 4. Generate PDF Document
    # ---------------------------------------------------------
    # The PDF uses its own stylesheet (pdf_cv.css) instead of style.css:
    # it hides web-only elements and lays the content out for A4 paper.
    try:
        pdf_css = CSS(filename='pdf_cv.css')

        HTML(string=html_output, base_url='.').write_pdf(
            'federico_baggio_cv.pdf',
            stylesheets=[pdf_css],
            pdf_identifier=PDF_IDENTIFIER,
        )
        print("[INFO] PDF generated: federico_baggio_cv.pdf")
        
    except Exception as e:
        print(f"[WARNING] PDF generation failed: {e}")

if __name__ == "__main__":
    build_cv()