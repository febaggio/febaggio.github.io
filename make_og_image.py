"""
Generate og-image.png, the 1200x630 preview shown when the site is shared on
LinkedIn, WhatsApp, Slack and similar.

This is deliberately NOT part of build.py: the image only changes when the
name or tagline does, and generating it needs a network round-trip for the
web fonts. Run it by hand and commit the result:

    python make_og_image.py
"""

import io

import pymupdf
import yaml
from weasyprint import HTML

WIDTH, HEIGHT = 1200, 630

CARD = """
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Roboto+Mono:wght@400;700&display=swap');
  @page {{ size: {w}px {h}px; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
      width: {w}px; height: {h}px;
      background: #fcfaf7;
      font-family: 'Inter', sans-serif;
      color: #1a1a1a;
      padding: 90px 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
  }}
  .rule {{ width: 90px; height: 6px; background: #ff4d4d; margin-bottom: 46px; }}
  h1 {{ font-size: 76px; font-weight: 800; letter-spacing: -2px; line-height: 1; }}
  .subtitle {{
      font-family: 'Roboto Mono', monospace;
      font-size: 26px; color: #ff4d4d;
      margin-top: 22px; letter-spacing: 1px;
  }}
  .bio {{ font-size: 27px; color: #666666; margin-top: 34px; }}
  .url {{
      font-family: 'Roboto Mono', monospace;
      font-size: 21px; color: #999999; margin-top: 52px;
  }}
</style></head>
<body>
  <div class="rule"></div>
  <h1>{name}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="bio">{bio}</p>
  <p class="url">{url}</p>
</body></html>
"""


def main():
    with io.open('cv_data.yaml', encoding='utf-8') as f:
        info = yaml.safe_load(f)['info']

    html = CARD.format(
        w=WIDTH, h=HEIGHT,
        name=info['name'],
        subtitle=info['subtitle'],
        bio=info['bio'],
        url=info['site_url'].split('//')[-1],
    )

    # WeasyPrint renders to PDF, PyMuPDF rasterises it. The PDF is laid out in
    # points (72/inch) while our CSS is in px (96/inch), hence the 96/72 zoom.
    pdf = HTML(string=html).write_pdf()
    page = pymupdf.open(stream=pdf, filetype='pdf')[0]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(96 / 72, 96 / 72))
    pix.save('og-image.png')
    print(f"[INFO] og-image.png written ({pix.width}x{pix.height})")


if __name__ == '__main__':
    main()
