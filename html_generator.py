#!/usr/bin/env python3
"""
HTML Resume Generator using JSON Template Configuration
Converts JSON resume data to professional HTML output using JSON-based templates
"""

import argparse
import json
import sys


class HTMLResumeGenerator:
    def __init__(self, template_file="html_template.json"):
        """Initialize the HTML generator with JSON template configuration"""
        self.template_file = template_file
        self.template = self.load_template()

    def load_template(self):
        """Load the JSON template configuration"""
        try:
            with open(self.template_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Template file '{self.template_file}' not found.")
            return None

    def render_value(self, template_str, data):
        """Simple template variable replacement"""
        if not isinstance(template_str, str):
            return template_str

        # Replace {{ name }} style variables
        result = template_str
        if "{{ name }}" in result and "name" in data:
            result = result.replace("{{ name }}", data["name"])

        return result

    def generate_css(self):
        """Generate CSS from JSON template configuration"""
        if "css" not in self.template:
            return ""

        css_config = self.template["css"]
        css_parts = []

        # Process each CSS section
        for section_name, section_rules in css_config.items():
            css_parts.append(self._process_css_section(section_rules))

        return "\n".join(css_parts)

    def _process_css_section(self, rules):
        """Process a CSS section and return formatted CSS"""
        css_lines = []

        for selector, properties in rules.items():
            if selector.startswith("@"):
                # Handle @page, @media queries
                css_lines.append(f"{selector} {{")
                if isinstance(properties, dict):
                    for nested_selector, nested_props in properties.items():
                        if isinstance(nested_props, dict):
                            css_lines.append(f"    {nested_selector} {{")
                            for prop, value in nested_props.items():
                                processed_value = self._process_template_value(value)
                                css_lines.append(f"        {prop}: {processed_value};")
                            css_lines.append("    }")
                        else:
                            processed_value = self._process_template_value(nested_props)
                            css_lines.append(f"    {nested_selector}: {processed_value};")
                css_lines.append("}")
            elif isinstance(properties, dict):
                # Regular CSS rule
                css_lines.append(f"{selector} {{")
                for prop, value in properties.items():
                    # Replace template variables
                    processed_value = self._process_template_value(value)
                    css_lines.append(f"    {prop}: {processed_value};")
                css_lines.append("}")

        return "\n".join(css_lines)

    def _process_template_value(self, value):
        """Process template variables in CSS values"""
        if not isinstance(value, str):
            return str(value)

        # Handle template variables like {{ document.page_size }}
        result = value

        # Replace document variables
        if "{{ document." in result:
            doc = self.template.get("document", {})
            for key, val in doc.items():
                result = result.replace(f"{{{{ document.{key} }}}}", str(val))

        # Replace typography variables
        if "{{ typography." in result:
            typo = self.template.get("typography", {})
            for key, val in typo.items():
                result = result.replace(f"{{{{ typography.{key} }}}}", str(val))

        # Replace spacing variables
        if "{{ spacing." in result:
            spacing = self.template.get("spacing", {})
            for key, val in spacing.items():
                result = result.replace(f"{{{{ spacing.{key} }}}}", str(val))

        # Replace fonts variables
        if "{{ fonts." in result:
            fonts = self.template.get("fonts", {})
            for key, val in fonts.items():
                if key == "fallbacks" and "{{ fonts.fallbacks | join(', ') }}" in result:
                    joined_fonts = ", ".join([f'"{f}"' for f in val])
                    result = result.replace("{{ fonts.fallbacks | join(', ') }}", joined_fonts)
                else:
                    result = result.replace(f"{{{{ fonts.{key} }}}}", str(val))

        return result

    def generate_header_section(self, data):
        """Generate header HTML section"""
        html = '<div class="header">\n'
        html += f'    <div class="name">{data.get("name", "")}</div>\n'

        contact = data.get("contact", {})
        contact_parts = []

        if contact.get("phone"):
            contact_parts.append(contact["phone"])
        if contact.get("email"):
            contact_parts.append(f'<a href="mailto:{contact["email"]}">{contact["email"]}</a>')
        if contact.get("linkedin"):
            contact_parts.append(
                f'<a href="https://{contact["linkedin"]}">{contact["linkedin"]}</a>'
            )
        if contact.get("github"):
            contact_parts.append(f'<a href="https://{contact["github"]}">{contact["github"]}</a>')

        html += f'    <div class="contact">{" | ".join(contact_parts)}</div>\n'
        html += "</div>\n\n"
        return html

    def generate_summary_section(self, summary_text):
        """Generate summary section HTML"""
        html = '<div class="section">\n'
        html += '    <div class="section-title">Summary</div>\n'
        html += '    <div class="section-content">\n'
        html += f'        <div class="summary-text">{summary_text}</div>\n'
        html += "    </div>\n"
        html += "</div>\n\n"
        return html

    def generate_section(self, section_config, section_data, section_key):
        """Generate a section based on configuration"""
        if not section_data:
            return ""

        html = '<div class="section">\n'
        html += f'    <div class="section-title">{section_config["title"]}</div>\n'
        html += '    <div class="section-content">\n'

        if section_config["type"] == "two_column_entries":
            for entry in section_data:
                # Main row
                main_fields = section_config["fields"]["main"]
                html += '        <div class="entry">\n'
                html += (
                    f'            <div class="entry-main">{entry.get(main_fields[0], "")}</div>\n'
                )
                # For education section, locations should not be bold
                location_class = "entry-location" if section_key == "education" else "entry-date"
                html += f'            <div class="{location_class}">{entry.get(main_fields[1], "")}</div>\n'
                html += "        </div>\n"

                # Sub row
                sub_fields = section_config["fields"]["sub"]
                html += '        <div class="entry-sub">\n'
                html += f"            <div>{entry.get(sub_fields[0], '')}</div>\n"
                html += f"            <div>{entry.get(sub_fields[1], '')}</div>\n"
                html += "        </div>\n"

        elif section_config["type"] == "two_column_entries_with_items":
            for entry in section_data:
                # Main row
                main_fields = section_config["fields"]["main"]
                html += '        <div class="entry">\n'
                html += (
                    f'            <div class="entry-main">{entry.get(main_fields[0], "")}</div>\n'
                )
                html += (
                    f'            <div class="entry-date">{entry.get(main_fields[1], "")}</div>\n'
                )
                html += "        </div>\n"

                # Sub row
                sub_fields = section_config["fields"]["sub"]
                html += '        <div class="entry-sub">\n'
                html += f"            <div>{entry.get(sub_fields[0], '')}</div>\n"
                html += f"            <div>{entry.get(sub_fields[1], '')}</div>\n"
                html += "        </div>\n"

                # Items list
                items_field = section_config["fields"]["items"]
                if entry.get(items_field):
                    html += '        <ul class="item-list">\n'
                    for item in entry[items_field]:
                        html += f"            <li>{item}</li>\n"
                    html += "        </ul>\n"

        elif section_config["type"] == "project_entries":
            for entry in section_data:
                # Project header
                html += '        <div class="project-header">\n'
                html += "            <div>\n"
                project_name = entry.get("name", "")
                project_url = entry.get("url", "")
                if project_url:
                    html += f'                <span class="project-name"><a href="{project_url}">{project_name}</a></span> | \n'
                else:
                    html += (
                        f'                <span class="project-name">{project_name}</span> | \n'
                    )
                tech_list = entry.get("technologies", [])
                html += (
                    f'                <span class="project-tech">{", ".join(tech_list)}</span>\n'
                )
                html += "            </div>\n"
                html += f"            <div>{entry.get('date', '')}</div>\n"
                html += "        </div>\n"

                # Description items
                if entry.get("description"):
                    html += '        <ul class="item-list">\n'
                    for desc in entry["description"]:
                        html += f"            <li>{desc}</li>\n"
                    html += "        </ul>\n"

        elif section_config["type"] == "skills_list":
            html += '        <div class="skills-list">\n'
            for category, skills in section_data.items():
                html += '            <div class="skill-line">\n'
                html += f'                <span class="skill-category">{category}</span>: {", ".join(skills)}\n'
                html += "            </div>\n"
            html += "        </div>\n"

        html += "    </div>\n"  # Close section-content
        html += "</div>\n\n"  # Close section
        return html

    def generate_html_from_json(self, json_data):
        """Generate complete HTML from JSON data using JSON template"""
        if not self.template:
            return None

        # Start HTML document
        title = self.render_value(self.template["document"]["title"], json_data)
        google_fonts = self.template["fonts"]["google_fonts"]

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{google_fonts}" rel="stylesheet">
    <style>
        /* Ensure font loads with high priority */
        @import url('{google_fonts}');
        {self.generate_css()}
    </style>
</head>
<body>
'''

        # Generate header
        html += self.generate_header_section(json_data)

        # Generate summary section first if it exists
        if "summary" in json_data:
            html += self.generate_summary_section(json_data["summary"])

        # Generate sections based on template layout
        layout = self.template["layout"]["sections"]
        section_order = ["experience", "projects", "skills", "education"]

        for section_key in section_order:
            if section_key in layout and section_key in json_data:
                section_config = layout[section_key]
                section_data = json_data[section_key]
                html += self.generate_section(section_config, section_data, section_key)

        html += "</body>\n</html>"
        return html

    def save_html(self, html_content, output_file):
        """Save HTML content to file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML resume from JSON data using JSON template"
    )
    parser.add_argument("--input", default="resume_data.json", help="Input JSON file")
    parser.add_argument("--output", default="resume.html", help="Output HTML file")
    parser.add_argument("--template", default="html_template.json", help="JSON template file")

    args = parser.parse_args()

    # Load JSON data
    try:
        with open(args.input, encoding="utf-8") as f:
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
        print("Open in browser or print to PDF for final output.")
        return 0
    else:
        print("Failed to save HTML file.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
