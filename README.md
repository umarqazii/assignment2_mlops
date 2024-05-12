# Web Scraping and Data Versioning with Airflow, Git, and DVC

## Overview

This project demonstrates a workflow for web scraping news articles from specified websites using Airflow, and then versioning the scraped data using Git and Data Version Control (DVC).

## Project Structure

## Initialize DVC
dvc init

Run Airflow DAG
Copy mlops_a2.py to Airflow's DAGs directory (/opt/airflow/dags/).
Start the Airflow scheduler and web server.
Access the Airflow UI and trigger the mlops_a2 DAG to run manually or on schedule.
Verify Results
Check the articles.csv file in airflow/articles/ for scraped article data.
Use DVC commands (dvc status, dvc diff) to track changes and versions of articles.csv.
Contributing
Contributions to this project are welcome! Please feel free to submit issues or pull requests.

Resources
Airflow Documentation
Data Version Control (DVC) Documentation
Git Documentation
