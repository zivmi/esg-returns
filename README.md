# Do ESG factors relate to yields of companies?

This is a project built as a part of "Digital Tools for Finance" course at the University of Zurich, during the fall of 2023.

## Overview
This project analyzes how ESG (Environmental, Social, and Governance) factors relate to the yields of companies. It uses a Python script for analysis and LaTeX for report generation.

## Requirements
- Docker

Project Organization
------------

    ├── LICENSE
    ├── README.md                <- The top-level README for developers using this project
    ├── Dockerfile
    ├── build_project.py         <- Script to build the project. It runs all the scripts in the correct order.
    │                                       
    ├── data
    │   ├── processed             <- The final, canonical data sets for modeling
    │   ├── raw                   <- The original, immutable data dump
    │   └── financial_data.db     <- SQLite database containing all the data
    │        
    ├── notebooks                 <- Jupyter notebooks contained copy of the analysis, for fetching data
    │                                to fitting models. It also contains EDA and robustness checks.
    │    
    ├── reports                   <- Generated analysis as PDF, LaTeX and PNG
    │   ├── pdfs                  <- **THE FINAL REPORTS AND PRESENTATION**
    │   ├── tables           
    │   ├── tex      
    │   └── figures               <- Generated graphics and figures to be used in reporting
    │
    ├── src                       <- Source code for use in this project
    │   ├── data                  <- Scripts to download and process data
    │   │   ├── fetch_data.py
    │   │   ├── make_sql_db.py    <- Scripts to collect data into an SQLite database
    │   │   └── processing_data.py
    │   │
    │   └── models                <- Scripts to train models and then use trained models to make predictions
    │       └── regression.py
    └── requirements.txt          <- The requirements file for reproducing the analysis environment
                       
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
docker build -t esg-returns-app .
```
4. Run the container in the interactive mode:
```bash
docker run -it esg-returns-app bash
```
5. Inside the container you will be located in `esg_returns` folder. Here you can run the build script to fetch data, run the analysis and generate the report and presentation:
```bash
python build_project.py
```
The final report will be generated in the reports/pdfs directory inside the container. **Do not close the terminal where the container is running in the interactive mode and do not shut down the container yet.** To inspect all the generated files, you can copy the project from the container to your local machine.

6. Open another terminal. See the running containers, and copy the container ID (refered to later as <container_id>):
```bash
docker ps
```
Output 
```
CONTAINER ID   IMAGE            COMMAND       CREATED          STATUS          PORTS     NAMES
<container_id>   esg-returns-app   "bash"        1 minute ago   Up 1 minute              <container_name>
```

7. Copy the built project to your desired path (<your_desired_path>)
```bash
docker cp <container_id>:esg-returns <your_desired_path>
```
Now you can open the project in your local machine and inspect the generated files.