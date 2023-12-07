import subprocess
import os

project_path = os.getcwd()

# Path to the tex files
tex_path = 'reports/tex'

python_scripts = ['src/data/fetch_data.py',
                  'src/data/processing_data.py', 
                  'src/data/make_sql_db.py',
                  'src/models/regression.py']

def run_all_scripts(script_list):
    for script in script_list:
        subprocess.run(["python", script])


if __name__ == "__main__":
    run_all_scripts(python_scripts)

    # Change current working directory to tex directory 
    # This is necessary for bib file to be found by pdflatex
    os.chdir(tex_path)

    # Compile the latex files
    subprocess.run(["pdflatex", "report.tex"], check=True)
    subprocess.run(["pdflatex", "presentation.tex"], check=True)

    # Move pdf files to reports/pdfs
    os.rename('report.pdf', '../pdfs/report.pdf')
    os.rename('presentation.pdf', '../pdfs/presentation.pdf')

    os.chdir(project_path)


