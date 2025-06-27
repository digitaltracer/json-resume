import argparse
import json

from fpdf import FPDF

# --- Global Constants for Jake's Resume Template Style ---
PDF_WIDTH = 210  # A4 width in mm
MARGIN_LEFT = 15
MARGIN_RIGHT = 15
MARGIN_TOP = 15
MARGIN_BOTTOM = 15
CONTENT_WIDTH = PDF_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# Spacing constants to match Jake's template exactly
SECTION_SPACING = 5  # Space between sections
ENTRY_SPACING = 3  # Space between entries within a section
SPACE_AFTER_TITLE_LINE = 3  # Space after the horizontal rule under section title
BULLET_INDENT = 4
BULLET_CHAR = "•"  # Use bullet
CONTACT_SEPARATOR = " | "


# --- PDF Class ---
class JakeResumePDF(FPDF):
    def __init__(
        self,
        orientation="P",
        unit="mm",
        format="A4",
        font_family="Times",  # Use Times serif font like original
        base_font_size_pt=11,
        line_height_multiplier=1.2,
    ):
        super().__init__(orientation, unit, format)
        self.current_font_family = font_family
        self.base_font_size_pt = base_font_size_pt
        self.line_height_multiplier = line_height_multiplier

        # Font sizes matching Jake's template exactly
        self.font_size_name_pt = 20  # Large but not huge for name
        self.font_size_section_pt = 12  # Section titles
        self.font_size_body_pt = self.base_font_size_pt
        self.font_size_small_pt = self.base_font_size_pt - 1

        # Line heights
        self.line_height_mm = self.base_font_size_pt * 0.352778 * self.line_height_multiplier
        self.tight_line_height_mm = self.base_font_size_pt * 0.352778 * 1.0

        # Set default font
        self.set_font(self.current_font_family, "", self.base_font_size_pt)

        # Test if Unicode bullet works with this font, fallback to hyphen if not
        self.bullet_char = BULLET_CHAR
        try:
            self.get_string_width(self.bullet_char)
        except:
            self.bullet_char = "-"  # Fallback to hyphen if Unicode fails

    def header(self):
        pass

    def footer(self):
        pass

    def _set_font(self, style="", size_pt=None):
        if size_pt is None:
            size_pt = self.font_size_body_pt
        self.set_font(self.current_font_family, style, size_pt)

    def add_name_header(self, name):
        """Add centered name in clean typography (not all caps)"""
        self._set_font(style="B", size_pt=self.font_size_name_pt)
        self.cell(0, 10, name, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(2)

    def add_contact_info(self, contact_details):
        """Add centered contact info with underlined links"""
        self._set_font(size_pt=self.font_size_small_pt)
        contact_items = []

        if contact_details.get("phone"):
            contact_items.append(contact_details.get("phone"))
        if contact_details.get("email"):
            email = contact_details.get("email")
            contact_items.append(email)  # Could add underline formatting here
        if contact_details.get("linkedin"):
            linkedin = (
                contact_details.get("linkedin").replace("https://", "").replace("http://", "")
            )
            contact_items.append(linkedin)
        if contact_details.get("github"):
            github = contact_details.get("github").replace("https://", "").replace("http://", "")
            contact_items.append(github)

        contact_string = CONTACT_SEPARATOR.join(filter(None, contact_items))
        self.cell(0, 6, contact_string, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(SECTION_SPACING)

    def add_section_title(self, title):
        """Add section title with horizontal line underneath"""
        self._set_font(style="B", size_pt=self.font_size_section_pt)
        title_upper = title.upper()
        self.cell(0, 7, title_upper, new_x="LMARGIN", new_y="NEXT", align="L")

        # Add horizontal line
        self.set_line_width(0.4)
        current_y = self.get_y()
        self.line(self.get_x(), current_y, self.get_x() + CONTENT_WIDTH, current_y)
        self.ln(SPACE_AFTER_TITLE_LINE)

    def add_education_entry(self, entry):
        """Add education entry in exact Jake's format: University | Location, then Degree | Date"""
        # Line 1: University (bold) | Location
        university = entry.get("university", "")
        location = entry.get("location", "")  # We need to add location to our data

        self._set_font(style="B", size_pt=self.font_size_body_pt)
        location_width = 0
        if location:
            self._set_font(size_pt=self.font_size_body_pt)  # Regular font for measuring
            location_width = self.get_string_width(location) + 5

        # University name (bold)
        self._set_font(style="B", size_pt=self.font_size_body_pt)
        self.cell(CONTENT_WIDTH - location_width, self.line_height_mm, university, align="L")

        # Location (regular)
        if location:
            self._set_font(size_pt=self.font_size_body_pt)
            self.cell(
                location_width,
                self.line_height_mm,
                location,
                new_x="LMARGIN",
                new_y="NEXT",
                align="R",
            )
        else:
            self.ln()

        # Line 2: Degree (italics) | Date
        degree = entry.get("degree", "")
        date_str = entry.get("date", "")

        if degree or date_str:
            date_width = 0
            if date_str:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                date_width = self.get_string_width(date_str) + 5

            # Degree (italics)
            if degree:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                self.cell(CONTENT_WIDTH - date_width, self.line_height_mm, degree, align="L")

            # Date (italics)
            if date_str:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                self.cell(
                    date_width,
                    self.line_height_mm,
                    date_str,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="R",
                )
            else:
                self.ln()

        self.ln(ENTRY_SPACING)

    def add_experience_entry(self, entry):
        """Add experience entry in exact Jake's format: Title | Date, then Company | Location"""
        # Line 1: Job Title (bold) | Date range
        title = entry.get("title", "")
        dates = entry.get("dates", "")

        dates_width = 0
        if dates:
            self._set_font(size_pt=self.font_size_body_pt)
            dates_width = self.get_string_width(dates) + 5

        # Job title (bold)
        self._set_font(style="B", size_pt=self.font_size_body_pt)
        self.cell(CONTENT_WIDTH - dates_width, self.line_height_mm, title, align="L")

        # Dates (regular)
        if dates:
            self._set_font(size_pt=self.font_size_body_pt)
            self.cell(
                dates_width, self.line_height_mm, dates, new_x="LMARGIN", new_y="NEXT", align="R"
            )
        else:
            self.ln()

        # Line 2: Company (italics) | Location
        company = entry.get("company", "")
        location = entry.get("location", "")

        if company or location:
            location_width = 0
            if location:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                location_width = self.get_string_width(location) + 5

            # Company (italics)
            if company:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                self.cell(CONTENT_WIDTH - location_width, self.line_height_mm, company, align="L")

            # Location (italics)
            if location:
                self._set_font(style="I", size_pt=self.font_size_body_pt)
                self.cell(
                    location_width,
                    self.line_height_mm,
                    location,
                    new_x="LMARGIN",
                    new_y="NEXT",
                    align="R",
                )
            else:
                self.ln()

        # Bullet points for responsibilities
        if entry.get("responsibilities"):
            self._set_font(size_pt=self.font_size_body_pt)
            for resp in entry.get("responsibilities"):
                self.set_x(self.l_margin + BULLET_INDENT)
                bullet_text = f"{self.bullet_char} {resp}"
                self.multi_cell(
                    CONTENT_WIDTH - BULLET_INDENT,
                    self.tight_line_height_mm,
                    bullet_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                )

        self.ln(ENTRY_SPACING)

    def add_project_entry(self, entry):
        """Add project entry in Jake's format"""
        # Project name (bold) | Date
        project_name = entry.get("name", "")
        technologies = entry.get("technologies", [])
        if technologies:
            project_display = f"{project_name} | {', '.join(technologies)}"
        else:
            project_display = project_name

        date_str = entry.get("date", "")

        date_width = 0
        if date_str:
            self._set_font(size_pt=self.font_size_body_pt)
            date_width = self.get_string_width(date_str) + 5

        # Project name (bold)
        self._set_font(style="B", size_pt=self.font_size_body_pt)
        self.cell(CONTENT_WIDTH - date_width, self.line_height_mm, project_display, align="L")

        # Date
        if date_str:
            self._set_font(size_pt=self.font_size_body_pt)
            self.cell(
                date_width, self.line_height_mm, date_str, new_x="LMARGIN", new_y="NEXT", align="R"
            )
        else:
            self.ln()

        # Bullet points for description
        if entry.get("description"):
            self._set_font(size_pt=self.font_size_body_pt)
            for desc in entry.get("description"):
                self.set_x(self.l_margin + BULLET_INDENT)
                bullet_text = f"{self.bullet_char} {desc}"
                self.multi_cell(
                    CONTENT_WIDTH - BULLET_INDENT,
                    self.tight_line_height_mm,
                    bullet_text,
                    new_x="LMARGIN",
                    new_y="NEXT",
                )

        self.ln(ENTRY_SPACING)

    def add_skills_section(self, skills_data):
        """Add skills section in Jake's format with bold categories"""
        self._set_font(size_pt=self.font_size_body_pt)

        for category, skill_list in skills_data.items():
            # Bold category name followed by colon
            self._set_font(style="B", size_pt=self.font_size_body_pt)
            category_text = f"{category}: "
            category_width = self.get_string_width(category_text)

            self.cell(category_width, self.line_height_mm, category_text, align="L")

            # Skills in regular font
            self._set_font(size_pt=self.font_size_body_pt)
            skills_text = ", ".join(skill_list)
            self.multi_cell(
                CONTENT_WIDTH - category_width,
                self.line_height_mm,
                skills_text,
                new_x="LMARGIN",
                new_y="NEXT",
            )

        self.ln(ENTRY_SPACING)


# --- Main Function ---
def create_resume(data, output_filename, font_family, base_font_size_pt, line_height_multiplier):
    pdf = JakeResumePDF(
        orientation="P",
        unit="mm",
        format="A4",
        font_family=font_family,
        base_font_size_pt=base_font_size_pt,
        line_height_multiplier=line_height_multiplier,
    )
    pdf.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
    pdf.set_margins(MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT)
    pdf.add_page()

    # Header with name (not all caps)
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
            "title": "Technical Skills",
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

            pdf.ln(SECTION_SPACING)

    pdf.output(output_filename)
    print(f"Jake's style resume saved to {output_filename}")


# --- Main execution block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Jake's Resume style PDF from JSON data."
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
        "--font-family",
        type=str,
        default="Times",
        choices=["Helvetica", "Arial", "Times", "Courier"],
        help="Base font family for the resume (default: Times)",
    )
    parser.add_argument(
        "--font-size-body",
        type=int,
        default=11,
        help="Base font size in points for body text (default: 11)",
    )
    parser.add_argument(
        "--line-height-multiplier",
        type=float,
        default=1.2,
        help="Multiplier for line height based on font size (default: 1.2)",
    )

    args = parser.parse_args()

    try:
        with open(args.input_file, encoding="utf-8") as f:
            resume_data = json.load(f)

        create_resume(
            data=resume_data,
            output_filename=args.output_file,
            font_family=args.font_family,
            base_font_size_pt=args.font_size_body,
            line_height_multiplier=args.line_height_multiplier,
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
