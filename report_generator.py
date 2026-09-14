#!/usr/bin/env python3
"""
Mediroza Pentest — M4 Report Generator
======================================
Compiles the Markdown report sections into a single PDF
using Jinja2 + WeasyPrint (or markdown → HTML → PDF).

Usage:
    python scripts/report_generator.py
"""
import argparse
from pathlib import Path

import markdown
from jinja2 import Template

from utils.config import ROOT, M4_DIR
from utils.logger import banner, info, success, warning


DOCS_DIR = ROOT / "docs"
REPORT_DIR = ROOT / "report"
REPORT_DIR.mkdir(exist_ok=True)

HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Mediroza Pentest Report</title>
<style>
  body { font-family: 'Helvetica', sans-serif; margin: 40px;
         color: #1f2937; line-height: 1.6; }
  h1 { color: #0f172a; border-bottom: 3px solid #0ea5e9;
       padding-bottom: 8px; }
  h2 { color: #0369a1; margin-top: 32px; }
  h3 { color: #075985; }
  code { background: #f1f5f9; padding: 2px 6px;
         border-radius: 4px; font-size: 0.9em; }
  pre  { background: #0f172a; color: #e2e8f0; padding: 16px;
         border-radius: 8px; overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; margin: 16px 0; }
  th, td { border: 1px solid #cbd5e1; padding: 8px 12px;
           text-align: left; }
  th { background: #0ea5e9; color: white; }
  blockquote { border-left: 4px solid #f59e0b; margin: 16px 0;
               padding: 8px 16px; background: #fffbeb; }
</style>
</head>
<body>
{{ content }}
</body>
</html>
""")


def load_sections(docs_dir: Path) -> str:
    """Concatenate all report markdown files in order."""
    files = sorted(docs_dir.glob("*.md"))
    info(f"Found {len(files)} sections.")
    md_text = "\n\n---\n\n".join(f.read_text() for f in files)
    return md_text


def render_html(md_text: str, outfile: Path) -> None:
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "codehilite"],
    )
    full_html = HTML_TEMPLATE.render(content=html_body)
    outfile.write_text(full_html)
    success(f"HTML report → {outfile}")


def render_pdf(html_file: Path, pdf_file: Path) -> None:
    try:
        from weasyprint import HTML
        HTML(filename=str(html_file)).write_pdf(str(pdf_file))
        success(f"PDF report → {pdf_file}")
    except ImportError:
        warning("weasyprint not installed. Install with: pip install weasyprint")
    except Exception as e:
        warning(f"PDF generation failed: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="M4 Report Generator")
    parser.add_argument("--docs", default=str(DOCS_DIR))
    args = parser.parse_args()

    banner("M4 Report Generator")

    docs_dir = Path(args.docs)
    if not docs_dir.exists():
        warning(f"Docs directory not found: {docs_dir}")
        return

    md_text = load_sections(docs_dir)
    html_file = REPORT_DIR / "Mediroza_Pentest_Report.html"
    pdf_file = REPORT_DIR / "Mediroza_Pentest_Report.pdf"

    render_html(md_text, html_file)
    render_pdf(html_file, pdf_file)


if __name__ == "__main__":
    main()