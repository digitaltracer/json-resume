#!/usr/bin/env python3
"""
Unified Resume to PDF Generator
Converts JSON resume data directly to PDF using HTML template and Playwright
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

# Import the HTML generator
from html_generator import HTMLResumeGenerator


def json_to_pdf(resume_json_path, output_pdf_path, template_path="html_template.json"):
    """
    Convert JSON resume data directly to PDF

    Args:
        resume_json_path (str): Path to JSON resume data
        output_pdf_path (str): Path for output PDF file
        template_path (str): Path to HTML template JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load JSON data
        with open(resume_json_path, encoding="utf-8") as f:
            resume_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Resume file '{resume_json_path}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False

    # Generate HTML
    generator = HTMLResumeGenerator(template_path)
    html_content = generator.generate_html_from_json(resume_data)

    if not html_content:
        print("Failed to generate HTML content.")
        return False

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as temp_html:
        temp_html.write(html_content)
        temp_html_path = temp_html.name

    try:
        # Convert HTML to PDF using Playwright
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to HTML file
            file_url = f"file://{Path(temp_html_path).resolve()}"
            page.goto(file_url)

            # Wait for network to be idle (fonts loaded)
            page.wait_for_load_state("networkidle")

            # Generate PDF
            page.pdf(
                path=output_pdf_path,
                format="letter",
                margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"},
            )

            # Clean up
            browser.close()

        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

    finally:
        # Clean up temporary HTML file
        try:
            Path(temp_html_path).unlink()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description="Convert JSON resume data directly to PDF")
    parser.add_argument("--input", default="resume_data.json", help="Input JSON resume file")
    parser.add_argument("--output", default="resume.pdf", help="Output PDF file")
    parser.add_argument("--template", default="html_template.json", help="HTML template JSON file")

    args = parser.parse_args()

    # Generate PDF
    if json_to_pdf(args.input, args.output, args.template):
        print(f"✅ PDF generated successfully: {args.output}")
        return 0
    else:
        print("❌ Failed to generate PDF.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
