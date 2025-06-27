# Resume PDF Generator (LaTeX-based)

This Python script generates a high-fidelity PDF resume from a JSON data file by programmatically creating a LaTeX (`.tex`) file and then compiling it using a standard LaTeX distribution (e.g., `pdflatex`). This approach ensures the final PDF matches the precise styling and layout of the target "Jake's Resume" LaTeX template.

## Prerequisites

- Python 3.x
- [uv](https://github.com/astral-sh/uv) (recommended, for package management)
- **A working LaTeX Distribution:**
    - You must have a LaTeX distribution installed on your system, such as TeX Live, MiKTeX (Windows), or MacTeX (macOS).
    - The LaTeX compiler (e.g., `pdflatex`) must be available in your system's PATH.
    - You can check by opening a terminal and typing `pdflatex --version`.
    - For installation guides, see:
        - TeX Live: [https://www.tug.org/texlive/](https://www.tug.org/texlive/)
        - MiKTeX: [https://miktex.org/](https://miktex.org/)
        - MacTeX: [https://www.tug.org/mactex/](https://www.tug.org/mactex/)

## Project Setup & Dependencies

This project uses `uv` for package management and `ruff` for linting and formatting. Dependencies include `pylatex` for generating LaTeX code.

1.  **Install `uv`**:
    If you don't have `uv`, install it first. Follow instructions from [uv's official documentation](https://github.com/astral-sh/uv#installation).
    ```bash
    pip install uv
    # or
    # curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create a virtual environment and sync dependencies**:
    From the project root directory:
    ```bash
    uv venv .venv
    source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
    uv sync --dev # Install main (pylatex) and development (ruff) dependencies
    ```

## Usage

1.  **Prepare your resume data:**
    Create a JSON file (e.g., `my_resume_data.json`) based on the structure of `resume_data.json`. Ensure all text uses characters compatible with LaTeX, or be prepared for potential encoding issues if using very unusual characters without proper LaTeX package support (though standard Unicode should largely work with `pdflatex` and `glyphtounicode`).

2.  **Run the script:**
    Execute the `resume_generator.py` script from your terminal. Ensure your virtual environment is active and LaTeX is installed.

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
    *   Generate an intermediate `.tex` file (e.g., `resume_temp.tex` in a temporary directory).
    *   Compile the `.tex` file using `pdflatex` (twice for cross-referencing).
    *   Save the final PDF as `jakes_resume.pdf` in the current directory.
    *   Clean up temporary files (unless `--keep-tex-file` is used).

    **Customized usage (CLI Options, assuming venv is active):**
    ```bash
    python resume_generator.py --input-file my_data.json --output-pdf-file my_resume.pdf --latex-compiler xelatex --keep-tex-file
    ```

### Command-Line Options

The script accepts the following command-line arguments:

*   `--input-file FILE_PATH`:
    *   Path to the JSON input file containing your resume data.
    *   Default: `resume_data.json`

*   `--output-pdf-file FILE_PATH`:
    *   Path where the final generated PDF resume will be saved.
    *   Default: `jakes_resume.pdf`

*   `--latex-compiler COMPILER_CMD`:
    *   The LaTeX compiler command to use (e.g., `pdflatex`, `xelatex`, `lualatex`).
    *   Default: `pdflatex`

*   `--keep-tex-file`:
    *   If specified, the intermediate `.tex` file will be saved in the same directory as the output PDF. Otherwise, it's cleaned up from a temporary location.

*   `-h, --help`:
    *   Show a help message listing all options and exit.

## Development - Linting and Formatting

This project uses `ruff` for code linting and formatting.
(Activate virtual environment first)
*   Format code: `ruff format .` or `uv run ruff format .`
*   Check & fix linting: `ruff check --fix .` or `uv run ruff check --fix .`

Ruff configuration is in `pyproject.toml`.

## Input Data Format (JSON)

The input JSON file structure remains the same as before (see `resume_data.json` for an example). Key fields include `name`, `contact`, `education`, `experience`, `projects`, and `skills`. The script will escape special LaTeX characters from your data where necessary.

## Script Overview (`resume_generator.py`)

The script now operates as follows:

1.  **Argument Parsing:** Handles CLI options for input JSON, output PDF, LaTeX compiler, and keeping intermediate files.
2.  **JSON Data Loading:** Reads the resume data from the specified JSON file.
3.  **LaTeX Code Generation (`pylatex`):**
    *   Initializes a `pylatex.Document` object.
    *   **Preamble Replication:** Adds all necessary LaTeX packages (`\usepackage`) and custom command definitions (`\newcommand`, `\renewcommand`) from the original `resume.tex` template to the document's preamble. This ensures the styling and structure are identical.
    *   **Body Construction:** Dynamically builds the LaTeX document body by inserting data from the JSON file into the predefined LaTeX structures (e.g., `\resumeSubheading{...}`, `\resumeItem{...}`). It handles escaping of special LaTeX characters in user-provided data.
4.  **Temporary File Management:** Saves the generated LaTeX code to a temporary `.tex` file.
5.  **LaTeX Compilation (`subprocess`):**
    *   Calls the specified LaTeX compiler (e.g., `pdflatex`) using Python's `subprocess` module.
    *   The compilation is run twice to ensure all cross-references and document elements (like table of contents, if any were used) are correctly generated.
    *   Includes error detection for the compilation process.
6.  **PDF Output and Cleanup:**
    *   If compilation is successful, the resulting PDF is moved to the user-specified output path.
    *   All temporary files (e.g., `.tex`, `.log`, `.aux`) are cleaned up, unless `--keep-tex-file` is specified, in which case the main `.tex` file is preserved.
7.  **Error Handling:** Includes checks for missing input files, JSON errors, and LaTeX compilation failures.

This new approach prioritizes achieving the exact visual fidelity of the original LaTeX resume template by using LaTeX itself as the rendering engine. The primary trade-off is the requirement for a LaTeX distribution to be installed on the system running the script.
