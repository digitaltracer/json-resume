#!/usr/bin/env python3
"""
HTML Resume Generator using JSON Template Configuration
Converts JSON resume data to professional HTML output using JSON-based templates
"""

import json
import argparse
import sys
from pathlib import Path


class HTMLResumeGenerator:
    def __init__(self, template_file="html_template.json"):
        """Initialize the HTML generator with JSON template configuration"""
        self.template_file = template_file
        self.template = self.load_template()
        
    def load_template(self):
        """Load the JSON template configuration"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
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
        t = self.template
        fonts = t["fonts"]
        typo = t["typography"] 
        spacing = t["spacing"]
        styles = t["styles"]
        doc = t["document"]
        
        css = f"""
        @page {{
            size: {doc['page_size']};
            margin: {doc['margins']};
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "{fonts['primary']}", {', '.join([f'"{f}"' for f in fonts['fallbacks']])};
            font-size: {typo['base_font_size']};
            line-height: {typo['line_height']};
            color: black;
            max-width: {doc['max_width']};
            margin: 0 auto;
            padding: {doc['padding']};
            font-display: swap;
        }}
        
        /* Ensure font loading */
        .font-loading {{
            font-family: "{fonts['primary']}", {', '.join([f'"{f}"' for f in fonts['fallbacks']])};
        }}

        /* Header */
        .header {{
            text-align: center;
            margin-bottom: {spacing['header_margin_bottom']};
        }}

        .name {{
            font-size: {typo['name_size']};
            font-weight: {styles['name']['font_weight']};
            font-variant: {styles['name']['font_variant']};
            margin-bottom: {spacing['name_margin_bottom']};
        }}

        .contact {{
            font-size: {typo['contact_size']};
            color: {styles['contact']['color']};
        }}

        .contact a {{
            color: {styles['links']['color']};
            text-decoration: {styles['links']['text_decoration']};
        }}

        /* Sections */
        .section {{
            margin-bottom: {spacing['section_margin_bottom']};
        }}

        .section-title {{
            font-size: {typo['section_title_size']};
            font-variant: {styles['section_title']['font_variant']};
            font-weight: {styles['section_title']['font_weight']};
            margin-bottom: {spacing['section_title_margin_bottom']};
            border-bottom: {styles['section_title']['border_bottom']};
            padding-bottom: {styles['section_title']['padding_bottom']};
        }}

        /* Two-column layout for entries */
        .entry {{
            display: flex;
            justify-content: space-between;
            margin-bottom: {spacing['entry_margin_bottom']};
        }}

        .entry-main {{
            font-weight: {styles['entry_main']['font_weight']};
        }}

        .entry-date {{
            font-weight: {styles['entry_date']['font_weight']};
        }}
        
        .entry-location {{
            font-weight: normal;
        }}

        .entry-sub {{
            display: flex;
            justify-content: space-between;
            margin-bottom: {spacing['entry_sub_margin_bottom']};
            font-style: {styles['entry_sub']['font_style']};
            font-size: {typo['small_size']};
        }}

        /* Bullet points */
        .item-list {{
            margin-left: {spacing['item_list_margin_left']};
            margin-bottom: {spacing['item_list_margin_bottom']};
        }}

        .item-list li {{
            margin-bottom: {spacing['item_margin_bottom']};
            list-style-type: disc;
            font-size: calc({typo['small_size']} * 1.01);
            line-height: 1.21;
        }}

        /* Projects specific */
        .project-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: {spacing['entry_margin_bottom']};
        }}

        .project-name {{
            font-weight: {styles['project_name']['font_weight']};
        }}

        .project-tech {{
            font-style: {styles['project_tech']['font_style']};
        }}

        /* Skills */
        .skills-list {{
            margin-left: {spacing['item_list_margin_left']};
        }}

        .skill-category {{
            font-weight: {styles['skill_category']['font_weight']};
        }}

        .skill-line {{
            margin-bottom: {spacing['skill_line_margin_bottom']};
            font-size: {typo['small_size']};
        }}

        /* Print styles */
        @media print {{
            body {{
                padding: 0;
                max-width: none;
                margin: 0;
            }}
        }}
        """
        return css
    
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
            contact_parts.append(f'<a href="https://{contact["linkedin"]}">{contact["linkedin"]}</a>')
        if contact.get("github"):
            contact_parts.append(f'<a href="https://{contact["github"]}">{contact["github"]}</a>')
        
        html += f'    <div class="contact">{" | ".join(contact_parts)}</div>\n'
        html += '</div>\n\n'
        return html
    
    def generate_section(self, section_config, section_data, section_key):
        """Generate a section based on configuration"""
        if not section_data:
            return ""
            
        html = f'<div class="section">\n'
        html += f'    <div class="section-title">{section_config["title"]}</div>\n'
        
        if section_config["type"] == "two_column_entries":
            for entry in section_data:
                # Main row
                main_fields = section_config["fields"]["main"]
                html += f'    <div class="entry">\n'
                html += f'        <div class="entry-main">{entry.get(main_fields[0], "")}</div>\n'
                # For education section, locations should not be bold
                location_class = "entry-location" if section_key == "education" else "entry-date"
                html += f'        <div class="{location_class}">{entry.get(main_fields[1], "")}</div>\n'
                html += f'    </div>\n'
                
                # Sub row
                sub_fields = section_config["fields"]["sub"]
                html += f'    <div class="entry-sub">\n'
                html += f'        <div>{entry.get(sub_fields[0], "")}</div>\n'
                html += f'        <div>{entry.get(sub_fields[1], "")}</div>\n'
                html += f'    </div>\n'
        
        elif section_config["type"] == "two_column_entries_with_items":
            for entry in section_data:
                # Main row
                main_fields = section_config["fields"]["main"]
                html += f'    <div class="entry">\n'
                html += f'        <div class="entry-main">{entry.get(main_fields[0], "")}</div>\n'
                html += f'        <div class="entry-date">{entry.get(main_fields[1], "")}</div>\n'
                html += f'    </div>\n'
                
                # Sub row
                sub_fields = section_config["fields"]["sub"]
                html += f'    <div class="entry-sub">\n'
                html += f'        <div>{entry.get(sub_fields[0], "")}</div>\n'
                html += f'        <div>{entry.get(sub_fields[1], "")}</div>\n'
                html += f'    </div>\n'
                
                # Items list
                items_field = section_config["fields"]["items"]
                if entry.get(items_field):
                    html += f'    <ul class="item-list">\n'
                    for item in entry[items_field]:
                        html += f'        <li>{item}</li>\n'
                    html += f'    </ul>\n'
        
        elif section_config["type"] == "project_entries":
            for entry in section_data:
                # Project header
                html += f'    <div class="project-header">\n'
                html += f'        <div>\n'
                html += f'            <span class="project-name">{entry.get("name", "")}</span> | \n'
                tech_list = entry.get("technologies", [])
                html += f'            <span class="project-tech">{", ".join(tech_list)}</span>\n'
                html += f'        </div>\n'
                html += f'        <div>{entry.get("date", "")}</div>\n'
                html += f'    </div>\n'
                
                # Description items
                if entry.get("description"):
                    html += f'    <ul class="item-list">\n'
                    for desc in entry["description"]:
                        html += f'        <li>{desc}</li>\n'
                    html += f'    </ul>\n'
        
        elif section_config["type"] == "skills_list":
            html += f'    <div class="skills-list">\n'
            for category, skills in section_data.items():
                html += f'        <div class="skill-line">\n'
                html += f'            <span class="skill-category">{category}</span>: {", ".join(skills)}\n'
                html += f'        </div>\n'
            html += f'    </div>\n'
        
        html += '</div>\n\n'
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
        
        # Generate sections based on template layout
        layout = self.template["layout"]["sections"]
        section_order = ["education", "experience", "projects", "skills"]
        
        for section_key in section_order:
            if section_key in layout and section_key in json_data:
                section_config = layout[section_key]
                section_data = json_data[section_key]
                html += self.generate_section(section_config, section_data, section_key)
        
        html += '</body>\n</html>'
        return html
    
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
    parser = argparse.ArgumentParser(description="Generate HTML resume from JSON data using JSON template")
    parser.add_argument("--input", default="resume_data.json", help="Input JSON file")
    parser.add_argument("--output", default="resume.html", help="Output HTML file")
    parser.add_argument("--template", default="html_template.json", help="JSON template file")
    
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