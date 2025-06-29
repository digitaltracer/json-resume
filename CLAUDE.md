# JSON Resume Generator - Project Structure

## Project Overview

This is a **JSON-driven resume generator** that creates professional HTML/CSS resumes from structured JSON data. The project aims to provide LaTeX-quality typography and formatting without requiring LaTeX dependencies, making it accessible to users who want high-quality resume generation with just Python and a web browser.

## Core Philosophy

- **JSON-First**: All configuration (fonts, spacing, colors, layout) is defined in JSON files
- **No LaTeX Dependencies**: Uses HTML/CSS to achieve professional typography
- **Template-Driven**: Flexible templating system allows easy customization
- **Print-Ready**: Generated HTML is optimized for browser PDF printing
- **Web Fonts**: Leverages Google Fonts for professional typography (Crimson Text as LaTeX Computer Modern alternative)

## Architecture

### Data Flow
```
resume_data.json → html_generator.py → resume.html → browser print → PDF
     ↑                    ↑
html_template.json    CSS generation
```

### Core Components

#### 1. **HTML Generator (`html_generator.py`)**
- **Purpose**: Main engine that converts JSON data to HTML
- **Key Features**:
  - Template-based CSS generation from JSON config
  - Section rendering based on layout configuration
  - Jinja2-style template variable replacement
  - Support for multiple section types (two-column, projects, skills)
- **Architecture**: Object-oriented with `HTMLResumeGenerator` class
- **Dependencies**: Pure Python with `json`, `argparse`, `pathlib`

#### 2. **Template Configuration (`html_template.json`)**
- **Purpose**: Complete styling and layout configuration
- **Structure**:
  - `document`: Page settings (margins, size, title)
  - `fonts`: Font family definitions and Google Fonts URLs
  - `typography`: Font sizes for all elements
  - `spacing`: Margins and padding throughout
  - `styles`: Font weights, variants, colors
  - `layout`: Section types and field mappings
- **Flexibility**: All visual aspects controllable via JSON

#### 3. **Resume Data (`resume_data.json`)**
- **Purpose**: Structured resume content
- **Sections**: `name`, `contact`, `education`, `experience`, `projects`, `skills`
- **Format**: Standard JSON with arrays for multi-entry sections
- **Flexibility**: Easy to modify content without touching code

#### 4. **PDF Generator (`pdf_generator.py`)**
- **Purpose**: High-quality PDF generation via browser automation
- **Technology**: Playwright (Chromium-based)
- **Features**:
  - Multiple page formats (Letter, A4, Legal)
  - Configurable margins (minimal, normal, generous)
  - Font loading optimization
  - Async PDF generation
- **Status**: Secondary tool (browser print is primary method)

#### 5. **Legacy Theme (`theme.json`)**
- **Purpose**: Alternative styling configuration
- **Status**: Legacy from earlier implementation
- **Contains**: PDF-specific settings, font configs, spacing in mm
- **Usage**: Not actively used by current HTML generator

## Implementation Details

### Section Types
The template system supports multiple section rendering types:

1. **`two_column_entries`**: Standard layout (title/date, subtitle/location)
   - Used for: Education
   - Fields: `main` (left column), `sub` (second row)

2. **`two_column_entries_with_items`**: Two-column with bullet points
   - Used for: Experience
   - Fields: `main`, `sub`, `items` (bullet list)

3. **`project_entries`**: Special project layout
   - Used for: Projects
   - Format: "Project Name | Tech Stack" with descriptions

4. **`skills_list`**: Category-based skills
   - Used for: Technical Skills
   - Format: "Category: skill1, skill2, skill3"

### CSS Generation Strategy
- Template-driven CSS generation from JSON config
- Responsive design with print media queries
- Font fallback system (Google Fonts → Local → Generic)
- LaTeX-inspired typography settings
- Consistent spacing system

### File Dependencies
- `html_generator.py` → `html_template.json` (required)
- `html_generator.py` → `resume_data.json` (default input)
- `pdf_generator.py` → Playwright (optional, for automation)
- `pyproject.toml` → Dependencies (ruff for linting)

## Development Architecture

### Code Quality
- **Linting**: Ruff with comprehensive rule set
- **Formatting**: Ruff with 99-character line length
- **Python Version**: 3.12+
- **Package Management**: UV for dependency management

### Extension Points
1. **New Section Types**: Add to `layout.sections` in template + implement in `generate_section()`
2. **Custom Styling**: Modify `html_template.json` for visual changes
3. **PDF Options**: Extend `pdf_generator.py` for advanced PDF features
4. **Data Sources**: Input can be any JSON matching the expected schema

## Usage Patterns

### Basic Generation
```bash
python3 html_generator.py --input resume_data.json --output resume.html
```

### Custom Templates
```bash
python3 html_generator.py --template custom_template.json
```

### PDF Generation
```bash
python3 pdf_generator.py resume.html resume.pdf --format letter --margins normal
```

## Future Enhancement Areas

1. **Multiple Templates**: Support for different resume styles
2. **Theme System**: Easy switching between visual themes
3. **Data Validation**: JSON schema validation for inputs
4. **CLI Improvements**: Better error handling and user feedback
5. **Export Formats**: Direct PDF generation without browser dependency
6. **Template Editor**: GUI for visual template customization

## Key Files Quick Reference

- `html_generator.py:282` - Main HTML generation function
- `html_generator.py:40` - CSS generation from JSON template
- `html_generator.py:203` - Section rendering logic
- `html_template.json:74` - Layout configuration
- `pdf_generator.py:147` - PDF generation entry point
- `pyproject.toml:17` - Ruff linting configuration

## Dependencies

### Required
- Python 3.12+
- Jinja2 (for template variable replacement)

### Optional
- Playwright (for automated PDF generation)
- UV (recommended package manager)
- Ruff (code formatting and linting)

### External
- Google Fonts (Crimson Text)
- Web browser (for PDF printing)

This architecture provides a solid foundation for extending the resume generator while maintaining simplicity and configurability.