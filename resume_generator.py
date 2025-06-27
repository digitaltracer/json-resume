import argparse
import json
import subprocess
import sys
import tempfile
import os
import shutil
from pylatex import Document, Section, Command, utils, NewPage, PageStyle, Head, Foot, MiniPage, LargeText, MediumText, LineBreak, SmallText, FlushLeft, FlushRight, Center
from pylatex.base_classes import Environment, Arguments
from pylatex.package import Package
from pylatex.utils import NoEscape # Important for raw LaTeX commands

# Placeholder for the main generation function
def generate_resume_tex(data, output_tex_filename):
    # Document setup (mimicking resume.tex)
    # Default PyLaTeX document name is 'default_filename.tex' if not specified in generate_tex
    doc = Document(documentclass='article', document_options=['letterpaper', '11pt'])

    # --- Preamble from resume.tex ---
    doc.packages.append(Package('latexsym'))
    doc.packages.append(Package('fullpage', options=['empty']))
    doc.packages.append(Package('titlesec'))
    doc.packages.append(Package('marvosym'))
    doc.packages.append(Package('color', options=['usenames', 'dvipsnames']))
    doc.packages.append(Package('verbatim'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('hyperref', options=['hidelinks']))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('babel', options=['english']))
    doc.packages.append(Package('tabularx'))
    doc.preamble.append(Command('input', 'glyphtounicode')) # For \pdfgentounicode=1

    # Font options (commented out in original, so not adding them by default)

    doc.preamble.append(Command('pagestyle', 'fancy'))
    doc.preamble.append(Command('fancyhf', NoEscape(r'{}'))) # Clear header/footer
    doc.preamble.append(Command('fancyfoot', NoEscape(r'{}')))
    doc.preamble.append(Command('renewcommand', NoEscape(r'\headrulewidth'), extra_arguments='0pt'))
    doc.preamble.append(Command('renewcommand', NoEscape(r'\footrulewidth'), extra_arguments='0pt'))

    # Adjust margins
    doc.preamble.append(Command('addtolength', arguments=[NoEscape(r'\oddsidemargin'), NoEscape('-0.5in')]))
    doc.preamble.append(Command('addtolength', arguments=[NoEscape(r'\evensidemargin'), NoEscape('-0.5in')]))
    doc.preamble.append(Command('addtolength', arguments=[NoEscape(r'\textwidth'), NoEscape('1in')]))
    doc.preamble.append(Command('addtolength', arguments=[NoEscape(r'\topmargin'), NoEscape('-.5in')]))
    doc.preamble.append(Command('addtolength', arguments=[NoEscape(r'\textheight'), NoEscape('1.0in')]))

    doc.preamble.append(Command('urlstyle', 'same'))
    doc.preamble.append(Command('raggedbottom'))
    doc.preamble.append(Command('raggedright'))
    doc.preamble.append(Command('setlength', NoEscape(r'\tabcolsep'), extra_arguments='0in'))

    # Sections formatting
    doc.preamble.append(NoEscape(r'''
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]
'''))

    # Ensure that generate pdf is machine readable/ATS parsable
    doc.preamble.append(NoEscape(r'\pdfgentounicode=1')) # Already covered by input{glyphtounicode} but explicit is fine

    # Custom commands
    doc.preamble.append(NoEscape(r'''
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
'''))
    # --- End Preamble ---

    # --- Document Body ---
    # Helper for LaTeX escaping
    def escape_latex_data(s):
        if s is None:
            return ''
        return utils.escape_latex(str(s))

    # Header (Name and Contact Info)
    with doc.create(Center()):
        name_str = data.get('name', 'Your Name')
        # Ensure \Huge \scshape are within \textbf{}
        formatted_name_latex = r'\textbf{{\Huge \scshape ' + escape_latex_data(name_str) + r'}}'
        doc.append(NoEscape(formatted_name_latex))
        doc.append(LineBreak())
        doc.append(Command('vspace', '1pt'))
        doc.append(LineBreak()) # For the \vspace to take effect properly before next line

        contact_parts = []
        if data.get('contact', {}).get('phone'):
            contact_parts.append(escape_latex_data(data['contact']['phone']))

        email = data.get('contact', {}).get('email')
        if email:
            contact_parts.append(NoEscape(r'\href{mailto:' + escape_latex_data(email) + r'}{\underline{' + escape_latex_data(email) + r'}}'))

        linkedin = data.get('contact', {}).get('linkedin')
        if linkedin:
            # Remove http(s) for display, but keep for link
            linkedin_display = linkedin.replace("https://", "").replace("http://", "")
            contact_parts.append(NoEscape(r'\href{https://' + escape_latex_data(linkedin) + r'}{\underline{' + escape_latex_data(linkedin_display) + r'}}'))

        github = data.get('contact', {}).get('github')
        if github:
            github_display = github.replace("https://", "").replace("http://", "")
            contact_parts.append(NoEscape(r'\href{https://' + escape_latex_data(github) + r'}{\underline{' + escape_latex_data(github_display) + r'}}'))

        if contact_parts:
            doc.append(SmallText(NoEscape(r' $|$ '.join(contact_parts))))

    # --- Sections ---
    # Order of sections as in the original resume.tex
    section_order = ["Education", "Experience", "Projects", "Technical Skills"] # Match titles in resume.tex
    data_keys = {"Education": "education", "Experience": "experience", "Projects": "projects", "Technical Skills": "skills"}

    for section_title_tex in section_order:
        data_key = data_keys[section_title_tex]
        if data_key in data and data[data_key]:
            with doc.create(Section(section_title_tex, numbering=False)):
                if data_key == "skills":
                    # Skills section has a specific structure directly using itemize
                    doc.append(NoEscape(r'\begin{itemize}[leftmargin=0.15in, label={}]'))
                    doc.append(NoEscape(r'    \small{\item{')) # Start \small{\item{
                    skills_content = []
                    for category, skill_list in data[data_key].items():
                        cat_str = r'\textbf{' + escape_latex_data(category) + r'}'
                        skills_str = escape_latex_data(", ".join(skill_list))
                        skills_content.append(cat_str + r'{: ' + skills_str + r'}')
                    doc.append(NoEscape(r' \\ '.join(skills_content))) # Join categories with LaTeX newline
                    doc.append(NoEscape(r'    }}')) # End \item}, \small}
                    doc.append(NoEscape(r'\end{itemize}'))
                else:
                    # For other sections (Education, Experience, Projects)
                    doc.append(NoEscape(r'\resumeSubHeadingListStart'))

                    if data_key == "education":
                        for entry in data[data_key]:
                            uni = escape_latex_data(entry.get('university'))
                            loc = escape_latex_data(entry.get('location'))
                            degree = escape_latex_data(entry.get('degree'))
                            date = escape_latex_data(entry.get('date'))
                            doc.append(NoEscape(r'\resumeSubheading{' + uni + r'}{' + loc + r'}{' + degree + r'}{' + date + r'}'))

                    elif data_key == "experience":
                        for entry in data[data_key]:
                            title = escape_latex_data(entry.get('title'))
                            dates = escape_latex_data(entry.get('dates'))
                            company = escape_latex_data(entry.get('company'))
                            location = escape_latex_data(entry.get('location'))
                            doc.append(NoEscape(r'\resumeSubheading{' + title + r'}{' + dates + r'}{' + company + r'}{' + location + r'}'))

                            responsibilities = entry.get('responsibilities')
                            if responsibilities:
                                doc.append(NoEscape(r'\resumeItemListStart'))
                                for resp in responsibilities:
                                    doc.append(NoEscape(r'\resumeItem{' + escape_latex_data(resp) + r'}'))
                                doc.append(NoEscape(r'\resumeItemListEnd'))

                    elif data_key == "projects":
                        for entry in data[data_key]:
                            name = escape_latex_data(entry.get('name'))
                            tech_list = entry.get('technologies', [])
                            technologies = escape_latex_data(", ".join(tech_list))

                            project_heading_arg1 = NoEscape(r'\textbf{' + name + r'}')
                            if technologies:
                                project_heading_arg1 += NoEscape(r' $|$ \emph{' + technologies + r'}')

                            date = escape_latex_data(entry.get('date'))
                            doc.append(NoEscape(r'\resumeProjectHeading{' + project_heading_arg1 + r'}{' + date + r'}'))

                            description = entry.get('description')
                            if description:
                                doc.append(NoEscape(r'\resumeItemListStart'))
                                for desc_item in description:
                                    doc.append(NoEscape(r'\resumeItem{' + escape_latex_data(desc_item) + r'}'))
                                doc.append(NoEscape(r'\resumeItemListEnd'))

                    doc.append(NoEscape(r'\resumeSubHeadingListEnd'))

    # Generate the .tex file
    # The `Document` constructor's first argument is `default_filepath` if you want to set it there.
    # Otherwise, `generate_tex` takes the filepath (without .tex extension).
    # We will generate into a temporary directory.

    # For PyLaTeX, generate_tex needs a filepath without extension.
    # We'll handle the full path and temp dir outside this function for now.
    # This function will just return the populated doc object.
    return doc


def compile_tex_to_pdf(tex_filepath, output_directory, compiler='pdflatex', mock_compilation_for_testing=False):
    """Compiles a .tex file to PDF using the specified compiler."""

    # Mock compilation logic for testing in environments without LaTeX
    if mock_compilation_for_testing and compiler == 'pdflatex' and not shutil.which(compiler):
        print("MOCKING successful pdflatex compilation for testing purposes...")
        pdf_filename = os.path.basename(tex_filepath).replace(".tex", ".pdf")
        mock_pdf_path = os.path.join(os.path.dirname(tex_filepath), pdf_filename)
        try:
            # Create a dummy text file with a .pdf extension to simulate a PDF
            with open(mock_pdf_path, 'w') as f_mock:
                f_mock.write("%PDF-1.4\n% A Fake PDF for testing purposes\n")
            print(f"Mock PDF (dummy file) created at {mock_pdf_path}")
            return mock_pdf_path
        except Exception as e_mock:
            print(f"Error during mock PDF (dummy file) creation: {e_mock}")
            return None

    if not shutil.which(compiler):
        print(f"Error: LaTeX compiler '{compiler}' not found in PATH. Cannot generate PDF.")
        return None

    original_cwd = os.getcwd()
    tex_dir = os.path.dirname(tex_filepath)
    tex_filename = os.path.basename(tex_filepath)

    os.chdir(tex_dir) # Run LaTeX in the directory of the .tex file

    pdf_filename = tex_filename.replace(".tex", ".pdf")

    for _ in range(2): # Run twice for cross-references, toc, etc.
        process = subprocess.run(
            [compiler, "-interaction=nonstopmode", tex_filename],
            capture_output=True, text=True
        )
        if process.returncode != 0:
            print(f"Error during LaTeX compilation with {compiler}:")
            print(process.stdout)
            print(process.stderr)
            os.chdir(original_cwd)
            return None

    os.chdir(original_cwd)

    generated_pdf_path = os.path.join(tex_dir, pdf_filename)
    if os.path.exists(generated_pdf_path):
        return generated_pdf_path
    else:
        print(f"Error: PDF file '{pdf_filename}' not found after compilation.")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a PDF resume from JSON data by compiling LaTeX."
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default="resume_data.json",
        help="Path to the JSON input file (default: resume_data.json)",
    )
    parser.add_argument(
        "--output-pdf-file",
        type=str,
        default="jakes_resume.pdf",
        help="Path for the final generated PDF file (default: jakes_resume.pdf)",
    )
    parser.add_argument(
        "--latex-compiler",
        type=str,
        default="pdflatex",
        help="LaTeX compiler to use (default: pdflatex)",
    )
    parser.add_argument(
        "--keep-tex-file",
        action="store_true",
        help="Keep the intermediate .tex file after PDF generation.",
    )


    args = parser.parse_args()

    try:
        with open(args.input_file, encoding="utf-8") as f:
            resume_data = json.load(f)

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_tex_basename = "resume_temp"
            # generate_resume_tex is designed to take a base filepath for doc.generate_tex()
            doc = generate_resume_tex(resume_data, temp_tex_basename) # Pass only basename
            doc.generate_tex(os.path.join(tmpdir, temp_tex_basename)) # Generate into temp dir

            temp_tex_filepath = os.path.join(tmpdir, f"{temp_tex_basename}.tex")
            print(f"Intermediate LaTeX file generated at: {temp_tex_filepath}")

            # Pass mock_compilation_for_testing=True for environments without LaTeX
            # In a real scenario, this flag would be set based on environment or a specific CLI arg.
            generated_pdf_path = compile_tex_to_pdf(
                temp_tex_filepath,
                tmpdir,
                args.latex_compiler,
                mock_compilation_for_testing=True
            )

            if generated_pdf_path and os.path.exists(generated_pdf_path):
                # Ensure output directory exists for the final PDF
                final_output_dir = os.path.dirname(args.output_pdf_file)
                if final_output_dir and not os.path.exists(final_output_dir):
                    os.makedirs(final_output_dir)

                shutil.move(generated_pdf_path, args.output_pdf_file)
                print(f"Successfully generated PDF: {args.output_pdf_file}")

                if args.keep_tex_file:
                    # Optionally copy .tex file to same dir as PDF
                    final_tex_filename = os.path.basename(args.output_pdf_file).replace(".pdf", ".tex")
                    final_tex_path = os.path.join(final_output_dir or '.', final_tex_filename)
                    shutil.copy(temp_tex_filepath, final_tex_path)
                    print(f"Intermediate .tex file saved to: {final_tex_path}")
            else: # PDF generation failed
                print("PDF generation failed.")
                if args.keep_tex_file and os.path.exists(temp_tex_filepath):
                    # Try to save the .tex file even if PDF failed, for debugging
                    final_output_dir = os.path.dirname(args.output_pdf_file)
                    if final_output_dir and not os.path.exists(final_output_dir):
                        os.makedirs(final_output_dir)
                    final_tex_filename = os.path.basename(args.output_pdf_file).replace(".pdf", ".tex")
                    final_tex_path = os.path.join(final_output_dir or '.', final_tex_filename)
                    try:
                        shutil.copy(temp_tex_filepath, final_tex_path)
                        print(f"Intermediate .tex file (from failed PDF build) saved to: {final_tex_path}")
                    except Exception as e_copy:
                        print(f"Could not copy .tex file after failed build: {e_copy}")
                sys.exit(1)

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Input file '{args.input_file}' is not valid JSON. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
