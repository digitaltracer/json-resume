#!/usr/bin/env python3
"""
PDF Generator using Playwright
Converts HTML resume files to PDF using browser automation
"""

import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_pdf(html_file_path, output_pdf_path):
    """
    Convert HTML file to PDF using Playwright
    
    Args:
        html_file_path (str): Path to input HTML file
        output_pdf_path (str): Path for output PDF file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert to absolute path for file:// URL
        html_path = Path(html_file_path).resolve()
        
        if not html_path.exists():
            print(f"Error: HTML file '{html_file_path}' not found.")
            return False
        
        # Create file:// URL
        file_url = f"file://{html_path}"
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to HTML file
            page.goto(file_url)
            
            # Wait for network to be idle (fonts loaded)
            page.wait_for_load_state("networkidle")
            
            # Generate PDF
            page.pdf(path=output_pdf_path, format="letter", margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"})
            
            # Clean up
            browser.close()
            
        return True
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert HTML resume to PDF using Playwright")
    parser.add_argument("html_file", help="Input HTML file path")
    parser.add_argument("pdf_file", help="Output PDF file path")
    
    args = parser.parse_args()
    
    # Generate PDF
    if html_to_pdf(args.html_file, args.pdf_file):
        print(f"PDF generated successfully: {args.pdf_file}")
        return 0
    else:
        print("Failed to generate PDF.")
        return 1


if __name__ == "__main__":
    sys.exit(main())