#!/usr/bin/env python3
"""
HTML Resume Generator using Jinja2 Templates
Converts JSON resume data to professional HTML output
"""

import json
import argparse
import sys
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader


class HTMLResumeGenerator:
    def __init__(self, template_file="resume_template.html"):
        """Initialize the HTML generator with template file"""
        self.template_file = template_file
        
    def load_template(self):
        """Load the Jinja2 template"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return Template(template_content)
        except FileNotFoundError:
            print(f"Error: Template file '{self.template_file}' not found.")
            return None
    
    def generate_html_from_json(self, json_data):
        """Generate HTML from JSON resume data"""
        template = self.load_template()
        if not template:
            return None
            
        try:
            # Render the template with JSON data
            html_content = template.render(**json_data)
            return html_content
        except Exception as e:
            print(f"Error rendering template: {e}")
            return None
    
    def save_html(self, html_content, output_file):
        """Save HTML content to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Generate HTML resume from JSON data")
    parser.add_argument("--input", default="resume_data.json", help="Input JSON file")
    parser.add_argument("--output", default="resume.html", help="Output HTML file")
    parser.add_argument("--template", default="resume_template.html", help="HTML template file")
    
    args = parser.parse_args()
    
    # Load JSON data
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return 1
    
    # Generate HTML
    generator = HTMLResumeGenerator(args.template)
    html_content = generator.generate_html_from_json(resume_data)
    
    if not html_content:
        print("Failed to generate HTML content.")
        return 1
    
    # Save HTML
    if generator.save_html(html_content, args.output):
        print(f"Generated HTML resume: {args.output}")
        print(f"Open in browser or print to PDF for final output.")
        return 0
    else:
        print("Failed to save HTML file.")
        return 1


if __name__ == "__main__":
    sys.exit(main())