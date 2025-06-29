# JSON Resume Generator

A **JSON-driven resume generator** that creates professional HTML/CSS resumes from structured JSON data and converts them to high-quality PDFs using Playwright. Achieve LaTeX-quality typography without LaTeX dependencies.

## 🚀 Quick Start

### One-Command PDF Generation
```bash
# Generate PDF directly from JSON (recommended)
python3 resume_to_pdf.py --input resume_data.json --output resume.pdf

# With custom theme
python3 resume_to_pdf.py --input resume_data.json --template modern_theme.json --output resume.pdf
```

### Step-by-Step Generation
```bash
# 1. Generate HTML
python3 html_generator.py --input resume_data.json --output resume.html

# 2. Convert to PDF
python3 pdf_generator.py resume.html resume.pdf
```

## ✨ Features

- **🎨 100% Theme Configurability**: All styling defined in JSON templates
- **📄 One-Command Workflow**: JSON → PDF in a single script
- **🖨️ Print-Ready**: Optimized for browser PDF printing
- **🎯 Professional Typography**: LaTeX-quality formatting with web fonts
- **🔧 No Dependencies**: Uses HTML/CSS instead of LaTeX
- **🎪 Multiple Themes**: Easy theme creation and switching

## 📁 Project Structure

```
json-resume/
├── resume_to_pdf.py        # 🎯 Main: JSON → PDF (one command)
├── html_generator.py       # HTML generation engine
├── pdf_generator.py        # HTML → PDF conversion
├── resume_data.json        # 📝 Resume content data
├── html_template.json      # 🎨 Complete theme configuration
├── theme.json             # Legacy theme file
└── pyproject.toml         # Dependencies
```

## 🎨 Theme System

### Complete Theme Configurability
All styling is defined in JSON templates with zero hardcoded CSS:

```json
{
  "document": {
    "page_size": "letter",
    "margins": "0.5in"
  },
  "fonts": {
    "primary": "Computer Modern Serif",
    "google_fonts": "https://..."
  },
  "typography": {
    "base_font_size": "11pt",
    "name_size": "24pt"
  },
  "spacing": {
    "section_margin_bottom": "9pt",
    "entry_margin_bottom": "2pt"
  },
  "css": {
    "header": {
      ".name": {
        "font-size": "{{ typography.name_size }}",
        "font-weight": "bold"
      }
    }
  }
}
```

### Creating Custom Themes
```bash
# Copy default theme
cp html_template.json my_theme.json

# Edit my_theme.json (change fonts, colors, spacing)

# Use custom theme
python3 resume_to_pdf.py --template my_theme.json --output resume.pdf
```

## 📋 Usage Examples

### Basic Usage
```bash
# Default settings
python3 resume_to_pdf.py

# Equivalent to:
python3 resume_to_pdf.py --input resume_data.json --template html_template.json --output resume.pdf
```

### Custom Configurations
```bash
# Different resume data
python3 resume_to_pdf.py --input john_resume.json --output john.pdf

# Different theme
python3 resume_to_pdf.py --template modern_theme.json --output resume_modern.pdf

# Full customization
python3 resume_to_pdf.py --input jane_resume.json --template minimal_theme.json --output jane_minimal.pdf
```

### Multiple Versions
```bash
# Same data, different themes
python3 resume_to_pdf.py --input resume_data.json --template classic_theme.json --output resume_classic.pdf
python3 resume_to_pdf.py --input resume_data.json --template modern_theme.json --output resume_modern.pdf
python3 resume_to_pdf.py --input resume_data.json --template minimal_theme.json --output resume_minimal.pdf
```

## 📝 Resume Data Format

Structure your resume data in `resume_data.json`:

```json
{
  "name": "Your Name",
  "contact": {
    "phone": "123-456-7890",
    "email": "you@example.com",
    "linkedin": "linkedin.com/in/you",
    "github": "github.com/you"
  },
  "education": [
    {
      "university": "University Name",
      "location": "City, State",
      "degree": "Degree Title",
      "date": "Start - End"
    }
  ],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "location": "City, State",
      "dates": "Start - End",
      "responsibilities": [
        "Achievement or responsibility",
        "Another achievement"
      ]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "technologies": ["Tech1", "Tech2"],
      "date": "Date",
      "description": [
        "Project description",
        "Key achievements"
      ]
    }
  ],
  "skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["React", "Flask"],
    "Tools": ["Git", "Docker"]
  }
}
```

## ⚙️ Installation

### Dependencies
```bash
# Install dependencies
pip install playwright

# Install browser
playwright install chromium
```

### Alternative with UV
```bash
# Using UV package manager
uv sync
uv run resume_to_pdf.py --input resume_data.json --output resume.pdf
```

## 🎛️ Advanced Theme Customization

### Typography Settings
```json
{
  "typography": {
    "base_font_size": "11pt",
    "line_height": "1.15",
    "name_size": "24pt",
    "section_title_size": "13pt",
    "contact_size": "9.5pt",
    "small_size": "9.5pt"
  }
}
```

### Layout Spacing
```json
{
  "spacing": {
    "header_margin_bottom": "15pt",
    "section_margin_bottom": "9pt",
    "section_content_margin_left": "15pt",
    "entry_margin_bottom": "2pt",
    "item_list_margin_left": "15pt"
  }
}
```

### Complete CSS Control
The theme system allows complete CSS customization through JSON:

```json
{
  "css": {
    "sections": {
      ".section-title": {
        "font-variant": "small-caps",
        "border-bottom": "0.5pt solid black",
        "color": "{{ custom.primary_color }}"
      }
    }
  }
}
```

## 🛠️ Development

### Code Quality
```bash
# Linting
uv run ruff check
uv run ruff format

# Type checking with ruff
uv run ruff check --select=F
```

### Architecture
- **JSON-First**: All configuration in JSON files
- **Template-Driven**: Zero hardcoded styling in Python
- **Modular Design**: Separate HTML generation and PDF conversion
- **Clean Separation**: Logic vs. presentation

## 📖 Legacy Workflows

### HTML-Only Generation
```bash
python3 html_generator.py --input resume_data.json --output resume.html
```

### HTML to PDF Conversion
```bash
python3 pdf_generator.py resume.html resume.pdf
```

## 🎯 Key Benefits

1. **One Command**: JSON → PDF directly
2. **Theme Flexibility**: Create unlimited themes via JSON
3. **Professional Output**: LaTeX-quality typography
4. **No LaTeX**: Pure HTML/CSS approach
5. **Web Fonts**: Google Fonts integration
6. **Print Optimized**: Perfect PDF generation
7. **Developer Friendly**: JSON configuration, not code

## 🤝 Contributing

The project follows a clean architecture with complete separation between content (JSON), presentation (CSS/themes), and logic (Python). All styling is externalized to JSON templates, making theme creation accessible without coding.

---

**Generate professional resumes with the simplicity of JSON and the power of modern web technologies!** 🚀