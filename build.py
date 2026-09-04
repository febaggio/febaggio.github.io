import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

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

    # ---------------------------------------------------------
    # 2. Render HTML Template
    # ---------------------------------------------------------
    try:
        # Set up the Jinja2 environment to load templates from the current directory
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')
        
        # Render the template with the data loaded from YAML
        html_output = template.render(data)
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
            stylesheets=[pdf_css] 
        )
        print("[INFO] PDF generated: federico_baggio_cv.pdf")
        
    except Exception as e:
        print(f"[WARNING] PDF generation failed: {e}")

if __name__ == "__main__":
    build_cv()