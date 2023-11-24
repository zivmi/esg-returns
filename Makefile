.PHONY: clean data requirements 

#################################################################################
# GLOBALS                                                                       #
#################################################################################

#PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
#PYTHON_INTERPRETER = python3

#ifeq (,$(shell which conda))
#HAS_CONDA=False
#else
#HAS_CONDA=True
#endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
#requirements: test_environment
#	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
#	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
#data: requirements
#	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Delete all compiled Python files
#clean:
#	find . -type f -name "*.py[co]" -delete
#	find . -type d -name "__pycache__" -delete


#################################################################################
# BUILD REPORT                                                                  #
#################################################################################

# Define the target to build the TeX document
report.pdf: reports/tex/report.tex
	pdflatex -output-directory=reports tex/report.tex

trash = $(shell find . -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.bcf" -o -name "*.run.xml" -o -name "*.synctex.gz")

clean:
	rm -f $(trash)


