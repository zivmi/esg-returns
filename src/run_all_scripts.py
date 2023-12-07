import subprocess



def run_all_scripts(scripts_list):
    for script in scripts_list:
        subprocess.run(["python", script])

def compile_latex(latex_file):
    subprocess.run(["pdflatex", latex_file])

if __name__ == "__main__":
    
    python_scripts = ['src/data/fetch_data.py', 'src/data/processing_data.py', 'src/data/make_sql_db.py', 'src/models/regression.py']

    
    latex_file = 'reports/tex/report.tex'

    run_all_scripts(python_scripts)
    compile_latex(latex_file)