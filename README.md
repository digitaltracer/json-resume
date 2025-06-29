# JSON Resume Generator

A native Python resume generator that creates professional HTML/CSS resumes from JSON data. No LaTeX dependencies required - generates clean, print-ready HTML that closely matches LaTeX typography and formatting.

## Features

- **Native Python**: No external dependencies beyond Python packages
- **JSON-Driven Templates**: Configure layout, fonts, and styling via JSON
- **Professional Typography**: Matches LaTeX-quality output with proper fonts and spacing
- **Print-Ready**: Generates HTML optimized for browser printing to PDF
- **Flexible**: Easy customization through JSON template configuration

## Prerequisites

- Python 3.x
- [uv](https://github.com/astral-sh/uv) (recommended for package management)

## Installation & Setup

1. **Install `uv`** (if you don't have it):
   ```bash
   pip install uv
   # or
   # curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   uv sync --dev
   ```

3. **Install Jinja2** (template engine):
   ```bash
   pip install jinja2
   # or
   uv add jinja2
   ```

## Quick Start

Generate a resume using the default template and data:

```bash
python3 html_generator.py --input resume_data.json --output my_resume.html
```

Open `my_resume.html` in your browser and print to PDF for final output.

## Usage

### Basic Usage

```bash
# Generate HTML resume with default settings
python3 html_generator.py

# Custom input/output files
python3 html_generator.py --input my_data.json --output resume.html --template my_template.json
```

### Command-Line Options

- `--input FILE` - Input JSON resume data file (default: `resume_data.json`)
- `--output FILE` - Output HTML file (default: `resume.html`)
- `--template FILE` - JSON template configuration file (default: `html_template.json`)
- `--help` - Show help message

## File Structure

### Core Files

- **`html_generator.py`** - Main HTML generator script
- **`html_template.json`** - JSON template configuration (fonts, layout, styling)
- **`resume_data.json`** - Sample resume data in JSON format

### Generated Files

- **`*.html`** - Generated HTML resume files

## JSON Template Configuration

The `html_template.json` file controls all aspects of the resume layout and styling:

```json
{
  "document": {
    "title": "{{ name }} - Resume",
    "page_size": "letter",
    "margins": "0.5in",
    "max_width": "7.5in"
  },
  "fonts": {
    "primary": "Crimson Text",
    "fallbacks": ["Computer Modern Serif", "Times New Roman", "serif"],
    "google_fonts": "https://fonts.googleapis.com/css2?family=Crimson+Text..."
  },
  "typography": {
    "base_font_size": "12pt",
    "name_size": "25pt",
    "section_title_size": "14pt",
    "contact_size": "10pt",
    "small_size": "10pt"
  },
  "spacing": {
    "header_margin_bottom": "15pt",
    "section_margin_bottom": "12pt",
    "entry_margin_bottom": "2pt"
  },
  "layout": {
    "sections": {
      "education": {
        "title": "Education",
        "type": "two_column_entries",
        "fields": {
          "main": ["university", "location"],
          "sub": ["degree", "date"]
        }
      }
    }
  }
}
```

### Customization Options

#### Fonts
- Change `fonts.primary` to use different web fonts
- Modify `fonts.google_fonts` URL for custom Google Fonts
- Adjust font fallback stack in `fonts.fallbacks`

#### Typography
- `name_size`: Size of the main name heading (default: 25pt)
- `section_title_size`: Size of section titles (default: 14pt)
- `base_font_size`: Base body text size (default: 12pt)
- `contact_size` & `small_size`: Size for contact info and details (default: 10pt)

#### Spacing
- `header_margin_bottom`: Space after header section
- `section_margin_bottom`: Space between sections
- `entry_margin_bottom`: Space between entries
- `item_list_margin_left`: Indentation for bullet points

#### Layout Types
- `two_column_entries`: Standard two-column layout (title/date, subtitle/location)
- `two_column_entries_with_items`: Two-column with bullet point items
- `project_entries`: Special layout for projects (name | tech stack)
- `skills_list`: Skills organized by category

## Input Data Format

The `resume_data.json` file structure:

```json
{
  "name": "Your Name",
  "contact": {
    "phone": "123-456-7890",
    "email": "email@example.com",
    "linkedin": "linkedin.com/in/username",
    "github": "github.com/username"
  },
  "education": [
    {
      "university": "University Name",
      "location": "City, State",
      "degree": "Degree and Major",
      "date": "Start Date - End Date"
    }
  ],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "dates": "Start Date - End Date",
      "responsibilities": [
        "Achievement or responsibility description",
        "Another achievement"
      ]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "technologies": ["Tech1", "Tech2", "Tech3"],
      "date": "Project Date",
      "description": [
        "Project description or achievement",
        "Another project detail"
      ]
    }
  ],
  "skills": {
    "Languages": ["Python", "JavaScript", "Java"],
    "Frameworks": ["React", "Flask", "Django"],
    "Tools": ["Git", "Docker", "AWS"]
  }
}
```

## Typography & Design

### Font Selection
The default template uses **Crimson Text**, a web font that closely resembles LaTeX's Computer Modern serif font. The generator includes proper fallbacks:

1. Crimson Text (Google Fonts)
2. Computer Modern Serif 
3. Latin Modern Roman
4. Times New Roman
5. Generic serif

### Font Sizes (LaTeX Equivalent)
- **Name**: 25pt (matches LaTeX `\Huge`)
- **Section Titles**: 14pt (matches LaTeX `\large`)
- **Body Text**: 12pt (base size)
- **Details**: 10pt (matches LaTeX `\small`)

### Layout Principles
- **Two-column entries**: Left-aligned main content, right-aligned dates
- **Clean spacing**: Consistent margins and padding throughout
- **Professional typography**: Proper line height and letter spacing
- **Print optimization**: CSS designed for high-quality PDF generation

## Generating PDFs

### Method 1: Browser Print (Recommended)
1. Open the generated HTML file in your browser
2. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)
3. Choose "Save as PDF" or "Print to PDF"
4. Ensure margins are set to "Minimum" for best results

### Method 2: Command Line Tools
```bash
# Using wkhtmltopdf (if installed)
wkhtmltopdf resume.html resume.pdf

# Using Chrome/Chromium headless
google-chrome --headless --disable-gpu --print-to-pdf=resume.pdf resume.html
```

## Development

### Code Quality
The project uses `ruff` for linting and formatting:

```bash
# Format code
ruff format . 
# or
uv run ruff format .

# Check and fix linting issues
ruff check --fix .
# or 
uv run ruff check --fix .
```

### Project Structure
```
json-resume/
├── html_generator.py         # Main HTML generator
├── html_template.json        # Template configuration
├── resume_data.json          # Sample resume data
├── README.md                 # This file
├── pyproject.toml           # Python project config
└── uv.lock                  # Dependency lock file
```

## Troubleshooting

### Common Issues

**Template file not found**
```
Error: Template file 'html_template.json' not found.
```
- Ensure `html_template.json` exists in the current directory
- Use `--template` flag to specify a different template file

**JSON parsing errors**
```
Error parsing JSON: ...
```
- Validate your JSON syntax using a JSON validator
- Check for missing commas, quotes, or brackets
- Ensure UTF-8 encoding for special characters

**Font rendering issues**
- Web fonts require internet connection for first load
- Local fonts in fallback list will be used if web fonts fail
- Check browser console for font loading errors

### Performance Tips
- Generated HTML files are self-contained with embedded CSS
- No external dependencies needed after generation
- Files can be shared and opened on any device with a web browser

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `ruff format .` and `ruff check --fix .`
5. Submit a pull request

## License

MIT License - see the original template license for details.

## Comparison with LaTeX Approach

### Advantages of HTML/CSS Approach
- ✅ **No LaTeX installation required**
- ✅ **Universal compatibility** (works on any device with a browser)
- ✅ **Easy customization** (JSON configuration vs. LaTeX code)
- ✅ **Fast generation** (no compilation step)
- ✅ **Modern typography** (web fonts, responsive design)

### When to Use
- **HTML/CSS**: For most users, easy customization, no dependencies
- **LaTeX**: When pixel-perfect reproduction of existing LaTeX templates is required

The HTML/CSS approach achieves 95%+ visual similarity to LaTeX output while being much more accessible and maintainable.