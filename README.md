# Resume PDF Generator

This Python script generates a PDF resume from a JSON data file, styled similarly to "Jake's Resume" template. It allows for customization of font family, base font size, and line height through command-line options.

## Prerequisites

- Python 3.x
- [uv](https://github.com/astral-sh/uv) (recommended, for package management)
- `fpdf2` (will be installed via `uv`)

## Project Setup & Dependencies

This project uses `uv` for package management and `ruff` for linting and formatting.

1.  **Install `uv`**:
    If you don't have `uv`, install it first. Follow instructions from [uv's official documentation](https://github.com/astral-sh/uv#installation). A common way is:
    ```bash
    pip install uv 
    # or
    # curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create a virtual environment and sync dependencies**:
    From the project root directory:
    ```bash
    uv venv .venv  # Create a virtual environment named .venv
    source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
    uv sync --dev # Install main and development dependencies (fpdf2, ruff)
    ```
    (You can later deactivate the virtual environment with `deactivate`)


## Usage

1.  **Prepare your resume data:**
    Create a JSON file (e.g., `my_resume_data.json`) based on the structure of `resume_data.json` (provided as an example). See the "Input Data Format" section below for details.
    *   Ensure all text uses standard characters compatible with Latin-1 encoding if using core PDF fonts (Helvetica, Times, Courier). This means using hyphens `-` instead of en-dashes `–`, and avoiding special Unicode symbols not covered by these fonts. If you need broader Unicode support, you would need to modify the script to embed a Unicode-compatible font file (e.g., DejaVuSans.ttf) using FPDF's `add_font()` method.

2.  **Run the script:**
    Execute the `resume_generator.py` script from your terminal. Ensure your virtual environment (with `fpdf2` installed) is active, or run via `uv run`:

    **Basic usage (defaults, assuming venv is active):**
    ```bash
    python resume_generator.py
    ```
    Or, using `uv run` (manages virtual environment context automatically):
    ```bash
    uv run python resume_generator.py
    ```
    This will:
    *   Look for `resume_data.json` in the current directory.
    *   Generate `resume_generated.pdf`.
    *   Use "Helvetica" font, 10pt base body size, and a 1.5 line height multiplier.

    **Customized usage (CLI Options, assuming venv is active):**
    ```bash
    python resume_generator.py --input-file my_data.json --output-file my_resume.pdf --font-family Times --font-size-body 11 --line-height-multiplier 1.4
    ```
    Or with `uv run`:
    ```bash
    uv run python resume_generator.py --input-file my_data.json --output-file my_resume.pdf --font-family Times --font-size-body 11 --line-height-multiplier 1.4
    ```

### Command-Line Options

The script accepts the following command-line arguments:

*   `--input-file FILE_PATH`:
    *   Path to the JSON input file containing your resume data.
    *   Default: `resume_data.json`

*   `--output-file FILE_PATH`:
    *   Path where the generated PDF resume will be saved.
    *   Default: `resume_generated.pdf`

*   `--font-family {Helvetica,Arial,Times,Courier}`:
    *   Specifies the base font family for the resume.
    *   `Arial` will be substituted by `Helvetica` by FPDF2 for core fonts. For true Arial, a font file would need to be added to the script.
    *   Default: `Helvetica`

*   `--font-size-body POINTS`:
    *   Sets the base font size in points for the body text. Other font sizes (e.g., for name, section titles) are derived proportionally from this value.
    *   Default: `10`

*   `--line-height-multiplier FLOAT`:
    *   A multiplier that adjusts the line height based on the font size. For example, `1.5` means the line height will be 1.5 times the (converted) font size.
    *   Default: `1.5`

*   `-h, --help`:
    *   Show a help message listing all options and exit.

**Example with multiple options:**
```bash
python resume_generator.py --font-family Arial --font-size-body 9 --line-height-multiplier 1.3 --input-file my_personal_data.json --output-file MyArialResume_v1.pdf
```

## Development - Linting and Formatting

This project uses `ruff` for code linting and formatting, managed via `uv`.

*   **Activate your virtual environment** if not already active:
    ```bash
    source .venv/bin/activate 
    ```
*   **Format code**:
    ```bash
    uv run ruff format .
    # or just 'ruff format .' if venv is active and ruff is in PATH
    ```
*   **Check for linting issues**:
    ```bash
    uv run ruff check .
    # or just 'ruff check .'
    ```
*   **Automatically fix linting issues (where possible)**:
    ```bash
    uv run ruff check --fix .
    # or just 'ruff check --fix .'
    ```
Ruff configuration is stored in `pyproject.toml` under `[tool.ruff]`.

## Input Data Format (JSON)

The input JSON file should follow this structure:

```json
{
  "name": "Your Full Name",
  "contact": {
    "phone": "(555) 123-4567",
    "email": "youremail@example.com",
    "linkedin": "linkedin.com/in/yourprofile",
    "github": "github.com/yourusername",
    "address": "Optional: 123 Your Street, Your City, ST 12345" 
  },
  "education": [
    {
      "degree": "Your Degree (e.g., M.S. in Computer Science)",
      "university": "University Name",
      "date": "Graduation Date (e.g., May 2020)",
      "gpa": "Optional: X.X/Y.Y",
      "courses": [
        "Optional: Relevant Course 1", "Relevant Course 2"
      ]
    }
    // Add more education entries if needed
  ],
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "dates": "Employment Dates (e.g., June 2020 - Present or Jan 2019 - Dec 2019)",
      "location": "City, ST",
      "responsibilities": [
        "Responsibility or achievement 1.",
        "Responsibility or achievement 2."
      ]
    }
    // Add more experience entries if needed
  ],
  "projects": [
    {
      "name": "Project Name",
      "technologies": ["Optional: Tech 1", "Tech 2"],
      "date": "Optional: Project Date/Year",
      "link": "Optional: github.com/yourusername/project",
      "description": [
        "Project description point 1.",
        "Project description point 2."
      ]
    }
    // Add more project entries if needed
  ],
  "skills": {
    "Category 1 (e.g., Languages)": ["Skill A", "Skill B", "Skill C"],
    "Category 2 (e.g., Frameworks)": ["Skill D", "Skill E"],
    // Add more skill categories and skills as needed
  }
}
```

### Notes on Data:
*   All fields are optional in terms of script execution, but a good resume will have most of them.
*   If a section (like "projects") is not needed, you can omit it entirely from the JSON or provide an empty list (e.g., `"projects": []`). The script will skip empty/missing sections.

## Script Overview (`resume_generator.py`)

*   **Argument Parsing (`argparse`):** Handles command-line options for customization.
*   **Global Constants:** Defines layout parameters like page width, margins, and fixed spacing elements.
*   **`ResumePDF` Class (inherits from `FPDF`):**
    *   Initialized with font family, base font size, and line height multiplier from CLI arguments.
    *   Derives various font sizes (for name, titles, body, etc.) from the base font size.
    *   Calculates line heights in millimeters based on font size and multiplier.
    *   Contains custom methods for adding different parts of the resume (e.g., `add_section_title`, `add_education_entry`).
    *   Handles text formatting, alignment, and drawing lines using the specified font settings.
*   **`create_resume(data, output_filename, ...)` Function:**
    *   Initializes the `ResumePDF` object with all provided settings.
    *   Iterates through the input `data` dictionary.
    *   Calls the appropriate `ResumePDF` methods to build the document.
    *   Saves the PDF to `output_filename`.
*   **Main Execution Block (`if __name__ == "__main__":`):**
    *   Parses command-line arguments.
    *   Loads data from the specified input JSON file.
    *   Calls `create_resume` with the parsed settings and data to generate the PDF.
    *   Includes error handling for file operations and JSON parsing.

This script provides a flexible way to generate styled PDF resumes and can be further customized by modifying the Python code for more advanced styling or new sections.
