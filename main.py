import subprocess
import os
import sys

def get_latex_file_input():
    """
    Get the LaTeX file path from command-line argument or terminal prompt.
    
    Returns:
        str: Path to the selected LaTeX file, or None if invalid or canceled.
    """
    def validate_path(file_path):
        # Strip quotes and normalize path
        file_path = file_path.strip('"\'').strip()
        file_path = os.path.normpath(file_path)
        if not file_path.lower().endswith('.tex'):
            print(f"Error: '{file_path}' does not have a .tex extension.")
            return None
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return None
        return file_path

    if len(sys.argv) == 2:
        # Use command-line argument if provided
        return validate_path(sys.argv[1])
    
    # Prompt user in terminal for file path
    print("Enter the path to the LaTeX (.tex) file (or 'quit' to exit):")
    file_path = input().strip()
    if file_path.lower() == 'quit':
        return None
    return validate_path(file_path)

def convert_latex_to_pdf(latex_file_path):
    """
    Convert a LaTeX file to PDF using latexmk.
    
    Args:
        latex_file_path (str): Path to the input LaTeX file.
    
    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    # Check if the file exists and has .tex extension
    if not os.path.isfile(latex_file_path):
        print(f"Error: File '{latex_file_path}' does not exist.")
        return False
    
    if not latex_file_path.lower().endswith('.tex'):
        print("Error: Input file must have a .tex extension.")
        return False
    
    # Get the directory and base filename
    file_dir = os.path.dirname(latex_file_path)
    file_base = os.path.splitext(os.path.basename(latex_file_path))[0]
    
    # Check if latexmk is available
    try:
        subprocess.run(['latexmk', '--version'], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: latexmk is not installed or not found in system PATH.")
        print("To install TeX Live on Windows:")
        print("1. Download TeX Live from https://www.tug.org/texlive/acquire-netinstall.html")
        print("2. Run the installer and follow the instructions to install TeX Live.")
        print("3. Add TeX Live's bin directory (e.g., C:\\texlive\\2023\\bin\\win32) to your system PATH.")
        print("   - Open System Properties > Advanced > Environment Variables.")
        print("   - Edit PATH and add the TeX Live bin directory.")
        print("4. Verify installation by running 'latexmk --version' in a new terminal.")
        return False

    # Run latexmk to compile the LaTeX file to PDF
    try:
        # Change to the file's directory to handle included files properly
        if file_dir:
            os.chdir(file_dir)
        
        # Run latexmk with PDFLaTeX
        result = subprocess.run(
            ['latexmk', '-pdf', '-pdflatex=pdflatex', file_base + '.tex'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Success: PDF generated at {os.path.join(file_dir, file_base + '.pdf')}")
            return True
        else:
            print("Error: LaTeX compilation failed.")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to execute latexmk. Details: {e}")
        return False
    except FileNotFoundError:
        print("Error: latexmk is not installed or not found in system PATH.")
        return False

def generate_sample_rfp_latex(output_path):
    """
    Generate a sample LaTeX file for an RFP response.
    
    Args:
        output_path (str): Path to save the sample .tex file.
    """
    latex_content = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{geometry}
\\usepackage{booktabs}
\\usepackage{hyperref}
\\usepackage{parskip}
\\geometry{a4paper, margin=1in}
\\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}

\\title{RFP Response - Sample}
\\author{RFP Automation AI Agent}
\\date{May 2025}

\\begin{document}

\\maketitle

\\section*{Response to Request for Proposal}

This is a sample RFP response generated for testing the LaTeX to PDF converter.

\\subsection*{Objectives}
\\begin{itemize}
    \\item Deliver a high-quality solution tailored to client needs.
    \\item Ensure timely and cost-effective implementation.
\\end{itemize}

\\subsection*{Compliance}
\\begin{table}[h]
    \\centering
    \\begin{tabular}{l c}
        \\toprule
        \\textbf{Requirement} & \\textbf{Compliance} \\\\
        \\midrule
        Scalability & Yes \\\\
        Security & Yes \\\\
        \\bottomrule
    \\end{tabular}
    \\caption{Compliance Summary}
\\end{table}

\\end{document}
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    print(f"Sample LaTeX file generated at: {output_path}")

if __name__ == "__main__":
    # Generate a sample LaTeX file if no input is provided
    latex_file = get_latex_file_input()
    if latex_file is None:
        sample_path = os.path.join(os.getcwd(), "sample_rfp_response.tex")
        generate_sample_rfp_latex(sample_path)
        latex_file = sample_path
    
    if latex_file:
        convert_latex_to_pdf(latex_file)
    else:
        print("No valid LaTeX file provided. Exiting.")
        sys.exit(1)