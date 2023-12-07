# Do ESG factors relate to yields of companies?

This is a project built as a part of "Digital Tools for Finance" course at the University of Zurich, during the fall of 2023.

## Overview
This project analyzes how ESG (Environmental, Social, and Governance) factors relate to the yields of companies. It uses a Python script for analysis and LaTeX for report generation.

## Requirements
- Docker
- Python 3.8

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project
    ├── Dockerfile
    ├── build_project.py
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling
    │   ├── raw            <- The original, immutable data dump
    │   └── financial_data.db
    │        
    ├── notebooks          <- Jupyter notebooks.
    │    
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── pdfs     
    │   ├── tables           
    │   ├── tex      
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── fetch_data.py
    │   │   ├── make_sql_db.py
    │   │   └── processing_data.py
    │   │
    │   └── models         <- Scripts to train models and then use trained models to make predictions
    │       └── regression.py
    └── requirements.txt   <- The requirements file for reproducing the analysis environment
                       
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Setup and Running

1. Clone the repository:
```
git clone https://github.com/zivmi/esg-returns
```
2. Navigate to the project directory:
```bash
cd esg-returns
```
3. Build the Docker image:
```bash
esg-returns (main) $ docker build -t esg-returns-app .
```
4. Run:
```bash
esg-returns (main) $ docker run -p 4000:5432 esg-returns-app
```
