import argparse
import json
import sys  # For sys.exit()

from fpdf import FPDF

# Global THEME dictionary, to be loaded from theme.json
THEME = {}

# --- Global Constants for Jake's Resume Template Style ---
# These will be replaced by values from THEME
# PDF_WIDTH = 210  # A4 width in mm
# MARGIN_LEFT = 15
# MARGIN_RIGHT = 15
# MARGIN_TOP = 15
# MARGIN_BOTTOM = 15
# CONTENT_WIDTH = PDF_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# Spacing constants to match Jake's template exactly
# SECTION_SPACING = 5  # Space between sections
# ENTRY_SPACING = 3  # Space between entries within a section
# SPACE_AFTER_TITLE_LINE = 3  # Space after the horizontal rule under section title
# BULLET_INDENT = 4
# BULLET_CHAR = "•"  # Use bullet
# CONTACT_SEPARATOR = " | "


# --- PDF Class ---
class JakeResumePDF(FPDF):
    def __init__(
        self,
        theme,  # Added theme parameter
        orientation="P",
        unit="mm",
        # format="A4", # Format will come from theme
        # font_family="Times",  # Use Times serif font like original
        # base_font_size_pt=11,
        # line_height_multiplier=1.2,
    ):
        self.theme = theme
        super().__init__(orientation, unit, self.theme.get("page_format", "A4"))

        # Initialize based on theme
        self.current_font_family = self.theme["font_config"]["family_serif"]
        self.base_font_size_pt = self.theme["font_config"]["base_size_pt"]

        # Content width calculation based on theme margins
        self.pdf_width = (
            210 if self.theme.get("page_format", "A4").lower() == "a4" else 215.9
        )  # Letter width
        self.margin_left = self.theme["page_margins_mm"]["left"]
        self.margin_right = self.theme["page_margins_mm"]["right"]
        self.margin_top = self.theme["page_margins_mm"]["top"]
        self.margin_bottom = self.theme["page_margins_mm"]["bottom"]
        self.content_width = self.pdf_width - self.margin_left - self.margin_right

        # Font sizes from theme
        self.font_size_name_pt = self.theme["font_config"]["name_size_pt"]
        self.font_size_section_pt = self.theme["font_config"]["section_title_size_pt"]
        self.font_size_body_pt = self.theme["font_config"]["body_size_pt"]
        self.font_size_small_pt = self.theme["font_config"][
            "contact_size_pt"
        ]  # Using contact_size_pt for small

        # Line heights from theme
        _pt_to_mm = self.theme["spacing_mm"]["pt_to_mm_factor"]
        self.line_height_mm = (
            self.font_size_body_pt
            * _pt_to_mm
            * self.theme["spacing_mm"]["general_line_height_multiplier"]
        )
        self.tight_line_height_mm = (
            self.font_size_body_pt
            * _pt_to_mm
            * self.theme["spacing_mm"]["description_line_height_multiplier"]
        )

        # Set default font
        self.set_font(self.current_font_family, "", self.base_font_size_pt)

        self.bullet_char = self.theme["layout_elements"]["bullet_char"]
        try:
            self.get_string_width(self.bullet_char)
        except Exception:
            self.bullet_char = "-"  # Fallback to hyphen if Unicode fails

    def header(self):
        pass

    def footer(self):
        pass

    def _set_font(self, style="", size_pt=None, font_family=None):
        if size_pt is None:
            size_pt = self.font_size_body_pt
        if font_family is None:
            font_family = self.current_font_family
        self.set_font(font_family, style, size_pt)

    def add_name_header(self, name):
        """Add centered name using theme styles"""
        name_style_info = self.theme["text_styles"]["name"]
        font_style = name_style_info.get("font_style", "B")
        processed_name = name.upper() if name_style_info.get("transform") == "UPPERCASE" else name

        self._set_font(style=font_style, size_pt=self.font_size_name_pt)
        # Using a fixed height for name cell, can be themed later if needed
        self.cell(0, 10, processed_name, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(self.theme["spacing_mm"]["after_name"])

    def add_contact_info(self, contact_details):
        """Add centered contact info using theme styles"""
        self._set_font(size_pt=self.font_size_small_pt)
        contact_items = []
        separator = self.theme["layout_elements"]["contact_separator"]
        underline_links = self.theme["layout_elements"]["underline_links"]
        link_color_hex = self.theme["colors_hex"]["link"]
        # Assuming hex_to_rgb is a utility function you might add or fpdf2 handles hex directly
        # For now, let's assume fpdf2 text_color can handle hex, or we convert it.
        # FPDF text_color expects R, G, B components.
        r, g, b = (
            int(link_color_hex[1:3], 16),
            int(link_color_hex[3:5], 16),
            int(link_color_hex[5:7], 16),
        )

        # Helper to add item, potentially with link and underline
        def add_contact_item(text, link_url=None):
            if link_url and underline_links:
                self.set_text_color(r, g, b)
                current_style = self.font_style  # Capture current style (B, I, etc.)
                self._set_font(style=current_style + "U", size_pt=self.font_size_small_pt)
                contact_items.append({"text": text, "link": link_url, "is_link": True})
                self.set_text_color(0, 0, 0)  # Reset to default text color
                self._set_font(style=current_style, size_pt=self.font_size_small_pt)
            elif link_url:  # Link but no underline
                self.set_text_color(r, g, b)
                contact_items.append({"text": text, "link": link_url, "is_link": True})
                self.set_text_color(0, 0, 0)
            else:
                contact_items.append({"text": text, "is_link": False})

        if contact_details.get("phone"):
            add_contact_item(contact_details.get("phone"))
        if contact_details.get("email"):
            email_text = contact_details.get("email")
            add_contact_item(email_text, f"mailto:{email_text}")
        if contact_details.get("linkedin"):
            linkedin_text = (
                contact_details.get("linkedin").replace("https://", "").replace("http://", "")
            )
            add_contact_item(linkedin_text, f"https://{contact_details.get('linkedin')}")
        if contact_details.get("github"):
            github_text = (
                contact_details.get("github").replace("https://", "").replace("http://", "")
            )
            add_contact_item(github_text, f"https://{contact_details.get('github')}")

        # Calculate width of each part to manually construct the line
        # This is complex if mixing styled (linked/underlined) and plain text in one cell() call
        # Alternative: use write_html or multiple cell calls. For simplicity with FPDF core, let's try multiple cells.

        # Centering the contact line:
        total_width = 0
        for item in contact_items:
            style_to_measure = (
                self.font_style + "U"
                if item.get("is_link") and underline_links
                else self.font_style
            )
            self._set_font(style=style_to_measure, size_pt=self.font_size_small_pt)
            total_width += self.get_string_width(item["text"])

        total_width += (
            self.get_string_width(separator) * (len(contact_items) - 1)
            if len(contact_items) > 1
            else 0
        )

        start_x = self.l_margin + (self.content_width - total_width) / 2
        self.set_x(start_x)

        for i, item_info in enumerate(contact_items):
            text = item_info["text"]
            link_url = item_info.get("link")

            current_text_style = self.font_style  # Default style from _set_font
            if item_info["is_link"] and underline_links:
                self.set_text_color(r, g, b)
                current_text_style += "U"
            elif item_info["is_link"]:
                self.set_text_color(r, g, b)

            self._set_font(style=current_text_style, size_pt=self.font_size_small_pt)
            item_width = self.get_string_width(text)
            self.cell(item_width, 6, text, link=link_url or "", align="L")

            if item_info["is_link"]:  # Reset color after link
                self.set_text_color(0, 0, 0)
            self._set_font(
                style=self.font_style, size_pt=self.font_size_small_pt
            )  # Reset font style

            if i < len(contact_items) - 1:
                self.cell(self.get_string_width(separator), 6, separator, align="L")

        self.ln(self.theme["spacing_mm"]["after_contact_block"])

    def add_section_title(self, title):
        """Add section title with horizontal line underneath using theme styles"""
        title_style_info = self.theme["text_styles"]["section_title"]
        font_style = title_style_info.get("font_style", "B")
        processed_title = (
            title.upper() if title_style_info.get("transform") == "UPPERCASE" else title
        )

        if self.theme["spacing_mm"]["before_section_title_vspace"] < 0:
            self.set_y(
                self.get_y() + self.theme["spacing_mm"]["before_section_title_vspace"]
            )  # Negative vspace

        self._set_font(style=font_style, size_pt=self.font_size_section_pt)
        self.cell(
            0, 7, processed_title, new_x="LMARGIN", new_y="NEXT", align="L"
        )  # Height 7mm is estimate

        # Add horizontal line
        rule_thickness_pt = self.theme["layout_elements"]["section_rule_thickness_pt"]
        rule_thickness_mm = rule_thickness_pt * self.theme["spacing_mm"]["pt_to_mm_factor"]
        self.set_line_width(rule_thickness_mm)

        # Set rule color if defined, though it's black by default
        rule_color_hex = self.theme["colors_hex"].get("section_rule", "#000000")
        r, g, b = (
            int(rule_color_hex[1:3], 16),
            int(rule_color_hex[3:5], 16),
            int(rule_color_hex[5:7], 16),
        )
        self.set_draw_color(r, g, b)

        current_y = self.get_y()
        self.line(self.get_x(), current_y, self.get_x() + self.content_width, current_y)
        self.set_draw_color(0, 0, 0)  # Reset draw color

        self.ln(self.theme["spacing_mm"]["after_section_title_rule_vspace"])

    def add_education_entry(self, entry):
        """Add education entry using theme styles"""
        university_style = self.theme["text_styles"]["education_university"].get("font_style", "B")
        degree_style = self.theme["text_styles"]["education_degree"].get("font_style", "I")

        # Line 1: University (bold) | Location
        university = entry.get("university", "")
        location = entry.get("location", "")

        self._set_font(style=university_style, size_pt=self.font_size_body_pt)
        location_width = 0
        if location:
            self._set_font(
                style="", size_pt=self.font_size_body_pt
            )  # Regular for measuring location
            location_width = self.get_string_width(location) + 5  # Add some padding

        self._set_font(style=university_style, size_pt=self.font_size_body_pt)
        self.cell(self.content_width - location_width, self.line_height_mm, university, align="L")

        if location:
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for location text
            self.cell(
                location_width,
                self.line_height_mm,
                location,
                new_x="LMARGIN",
                new_y="NEXT",
                align="R",
            )
        else:
            self.ln(self.line_height_mm)

        # Line 2: Degree (italics) | Date
        degree = entry.get("degree", "")
        date_str = entry.get("date", "")

        if degree or date_str:
            date_width = 0
            if date_str:
                self._set_font(
                    style=degree_style, size_pt=self.font_size_body_pt
                )  # Italic for measuring date
                date_width = self.get_string_width(date_str) + 5

            if degree:
                self._set_font(style=degree_style, size_pt=self.font_size_body_pt)
                self.cell(self.content_width - date_width, self.line_height_mm, degree, align="L")

            if date_str:
                self._set_font(
                    style=degree_style, size_pt=self.font_size_body_pt
                )  # Italic for date text
                self.cell(
                    date_width,
                    self.line_height_mm,
                    date_str,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="R",
                )
            else:
                self.ln(self.line_height_mm)

        self.ln(self.theme["spacing_mm"]["after_individual_entry_vspace"])

    def add_experience_entry(self, entry):
        """Add experience entry using theme styles"""
        title_style = self.theme["text_styles"]["experience_title"].get("font_style", "B")
        company_style = self.theme["text_styles"]["experience_company"].get("font_style", "I")

        # Line 1: Job Title (bold) | Date range
        title = entry.get("title", "")
        dates = entry.get("dates", "")

        dates_width = 0
        if dates:
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for measuring dates
            dates_width = self.get_string_width(dates) + 5

        self._set_font(style=title_style, size_pt=self.font_size_body_pt)
        self.cell(self.content_width - dates_width, self.line_height_mm, title, align="L")

        if dates:
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for dates text
            self.cell(
                dates_width, self.line_height_mm, dates, new_x="LMARGIN", new_y="NEXT", align="R"
            )
        else:
            self.ln(self.line_height_mm)

        # Line 2: Company (italics) | Location
        company = entry.get("company", "")
        location = entry.get("location", "")

        if company or location:
            location_width = 0
            if location:
                self._set_font(
                    style=company_style, size_pt=self.font_size_body_pt
                )  # Italic for measuring location
                location_width = self.get_string_width(location) + 5

            if company:
                self._set_font(style=company_style, size_pt=self.font_size_body_pt)
                self.cell(
                    self.content_width - location_width, self.line_height_mm, company, align="L"
                )

            if location:
                self._set_font(
                    style=company_style, size_pt=self.font_size_body_pt
                )  # Italic for location text
                self.cell(
                    location_width,
                    self.line_height_mm,
                    location,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="R",
                )
            else:
                self.ln(self.line_height_mm)

        # Bullet points for responsibilities
        if entry.get("responsibilities"):
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for bullets
            bullet_indent_mm = self.theme["spacing_mm"]["bullet_indent"]
            for resp in entry.get("responsibilities"):
                self.set_x(self.l_margin + bullet_indent_mm)
                # The bullet char itself might need different font size (e.g. tiny)
                # For now, use body size for simplicity of bullet text
                bullet_text = f"{self.bullet_char} {resp}"
                self.multi_cell(
                    self.content_width - bullet_indent_mm,
                    self.tight_line_height_mm,  # Use tight line height for descriptions
                    bullet_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
                if self.theme["spacing_mm"]["bullet_point_item_vspace_after"] != 0:
                    self.ln(self.theme["spacing_mm"]["bullet_point_item_vspace_after"])

            if self.theme["spacing_mm"]["after_bullet_block_vspace"] != 0:
                self.ln(self.theme["spacing_mm"]["after_bullet_block_vspace"])

        self.ln(self.theme["spacing_mm"]["after_individual_entry_vspace"])

    def add_project_entry(self, entry):
        """Add project entry using theme styles"""
        project_name_style = self.theme["text_styles"]["project_name_tech_name"].get(
            "font_style", "B"
        )
        tech_style = self.theme["text_styles"]["project_name_tech_technologies"].get(
            "font_style", "I"
        )

        project_name = entry.get("name", "")
        technologies = entry.get("technologies", [])

        # Project name (bold) and Technologies (italic) on the same line, separated by " | "
        # Need to calculate widths to do this properly or use write_html if formatting is complex

        date_str = entry.get("date", "")
        date_width = 0
        if date_str:
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for measuring date
            date_width = self.get_string_width(date_str) + 5

        # Constructing the project name + tech string part by part
        self.set_x(self.l_margin)
        name_tech_width_available = self.content_width - date_width

        # Project Name part
        self._set_font(style=project_name_style, size_pt=self.font_size_body_pt)
        self.cell(
            self.get_string_width(project_name), self.line_height_mm, project_name, align="L"
        )

        # Technologies part (if any)
        if technologies:
            self._set_font(style="", size_pt=self.font_size_body_pt)  # For separator
            separator = " | "
            self.cell(self.get_string_width(separator), self.line_height_mm, separator, align="L")

            self._set_font(style=tech_style, size_pt=self.font_size_body_pt)
            tech_text = ", ".join(technologies)
            # This is a simplification, assumes name + tech fits. Proper handling might need multi_cell or width check.
            self.cell(self.get_string_width(tech_text), self.line_height_mm, tech_text, align="L")

        # Date (aligned right)
        if date_str:
            # We need to set Y position correctly if name+tech wrapped, but cell() does not easily give that.
            # For now, assuming single line for name+tech part to place date correctly.
            current_y_before_date = self.get_y()
            self.set_xy(
                self.l_margin + name_tech_width_available, current_y_before_date
            )  # x is end of name_tech space
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for date
            self.cell(
                date_width, self.line_height_mm, date_str, new_x="LMARGIN", new_y="NEXT", align="R"
            )
        else:
            self.ln(self.line_height_mm)

        # Bullet points for description
        if entry.get("description"):
            self._set_font(style="", size_pt=self.font_size_body_pt)  # Regular for bullets
            bullet_indent_mm = self.theme["spacing_mm"]["bullet_indent"]
            for desc in entry.get("description"):
                self.set_x(self.l_margin + bullet_indent_mm)
                bullet_text = f"{self.bullet_char} {desc}"
                self.multi_cell(
                    self.content_width - bullet_indent_mm,
                    self.tight_line_height_mm,
                    bullet_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
                if self.theme["spacing_mm"]["bullet_point_item_vspace_after"] != 0:
                    self.ln(self.theme["spacing_mm"]["bullet_point_item_vspace_after"])

            if self.theme["spacing_mm"]["after_bullet_block_vspace"] != 0:
                self.ln(self.theme["spacing_mm"]["after_bullet_block_vspace"])

        self.ln(self.theme["spacing_mm"]["after_individual_entry_vspace"])

    def add_skills_section(self, skills_data):
        """Add skills section using theme styles"""
        self._set_font(style="", size_pt=self.font_size_body_pt)  # Default for this section

        for category, skill_list in skills_data.items():
            # Bold category name, then regular colon, then skills
            self._set_font(style="B", size_pt=self.font_size_body_pt)
            category_name_width = self.get_string_width(category)
            self.cell(category_name_width, self.line_height_mm, category, align="L")

            self._set_font(
                style="", size_pt=self.font_size_body_pt
            )  # Regular for colon and skills
            colon_text = ": "
            colon_width = self.get_string_width(colon_text)
            self.cell(colon_width, self.line_height_mm, colon_text, align="L")

            skills_text = ", ".join(skill_list)
            remaining_width = self.content_width - (category_name_width + colon_width)

            current_x_after_colon = self.get_x()

            if self.get_string_width(skills_text) <= remaining_width:
                self.cell(
                    remaining_width,
                    self.line_height_mm,
                    skills_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="L",
                )
            else:  # Skills text is too long, use multi_cell for it, starting after colon
                self.set_x(current_x_after_colon)  # Ensure multi_cell starts right after the colon
                self.multi_cell(
                    remaining_width,
                    self.line_height_mm,
                    skills_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="L",
                )
        # Spacing after the entire skills block is handled by the main loop's "after_section_block_vspace"


# --- Main Function ---
def create_resume(
    data, output_filename, theme
):  # Removed font_family, base_font_size_pt, line_height_multiplier
    pdf = JakeResumePDF(
        theme=theme,  # Pass the loaded theme
        orientation="P",  # Could also be themed
        unit="mm",  # Could also be themed
        # format parameter removed, taken from theme inside JakeResumePDF
    )
    pdf.set_auto_page_break(auto=True, margin=pdf.margin_bottom)  # Use themed margin
    pdf.set_margins(pdf.margin_left, pdf.margin_top, pdf.margin_right)
    pdf.add_page()

    # Optional initial top spacing from theme
    initial_spacing = theme.get("spacing_mm", {}).get("initial_top_spacing_mm", 0)
    if initial_spacing > 0:
        pdf.ln(initial_spacing)

    # Header with name
    pdf.add_name_header(data.get("name", "Your Name"))

    # Contact Info
    if "contact" in data:
        pdf.add_contact_info(data["contact"])

    # Sections in Jake's template order
    sections_config = [
        {
            "key": "education",
            "title": "Education",
            "handler": pdf.add_education_entry,
            "is_list": True,
        },
        {
            "key": "experience",
            "title": "Experience",
            "handler": pdf.add_experience_entry,
            "is_list": True,
        },
        {
            "key": "projects",
            "title": "Projects",
            "handler": pdf.add_project_entry,
            "is_list": True,
        },
        {
            "key": "skills",
            "title": "Technical Skills",  # Title from LaTeX
            "handler": pdf.add_skills_section,
            "is_list": False,
        },
    ]

    for section_conf in sections_config:
        section_key = section_conf["key"]
        if section_key in data and data[section_key]:
            pdf.add_section_title(section_conf["title"])

            if section_conf["is_list"]:
                for entry in data[section_key]:
                    section_conf["handler"](entry)
            else:
                section_conf["handler"](data[section_key])

            # Spacing after a whole section block
            if pdf.theme["spacing_mm"].get("after_section_block_vspace", 0) != 0:
                pdf.ln(pdf.theme["spacing_mm"]["after_section_block_vspace"])

    pdf.output(output_filename)
    print(f"Resume based on theme saved to {output_filename}")


# --- Main execution block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Jake's Resume style PDF from JSON data, using a theme.json for styling."
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default="resume_data.json",
        help="Path to the JSON input file (default: resume_data.json)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="jakes_resume.pdf",
        help="Path for the generated PDF file (default: jakes_resume.pdf)",
    )
    parser.add_argument(
        "--theme-file",
        type=str,
        default="theme.json",
        help="Path to the JSON theme file (default: theme.json)",
    )
    # Removed CLI args for font, font-size, line-height as they come from theme

    args = parser.parse_args()

    try:
        with open(args.theme_file, encoding="utf-8") as f:
            THEME = json.load(f)
    except FileNotFoundError:
        print(f"Error: Theme file '{args.theme_file}' not found. Exiting.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Theme file '{args.theme_file}' is not valid JSON. Details: {e}. Exiting.")
        sys.exit(1)

    try:
        with open(args.input_file, encoding="utf-8") as f:
            resume_data = json.load(f)

        create_resume(
            data=resume_data,
            output_filename=args.output_file,
            theme=THEME,  # Pass the loaded THEME dictionary
        )
    except FileNotFoundError:
        print(
            f"Error: Input file '{args.input_file}' not found. Please create it or specify a valid file."
        )
    except json.JSONDecodeError as e:
        print(f"Error: Input file '{args.input_file}' is not valid JSON. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback

        traceback.print_exc()
