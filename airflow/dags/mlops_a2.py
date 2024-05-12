from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import csv
import os

# Define the DAGs folder path
DAGS_FOLDER = '/opt/airflow/articles/'

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links

def extract_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').text.strip() if soup.find('h1') else ''
    description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ''
    return title, description

def save_to_csv(data, filename):
    # Ensure that the directory exists before saving the file
    os.makedirs(DAGS_FOLDER, exist_ok=True)
    
    filepath = os.path.join(DAGS_FOLDER, filename)  # Construct the full file path
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    dawn_links = extract_links('https://www.dawn.com/')
    bbc_links = extract_links('https://www.bbc.com/')

    articles = []

    for link in dawn_links:
        if link.startswith('https://www.dawn.com/'):
            title, description = extract_article(link)
            articles.append({'title': title, 'description': description, 'source': 'Dawn'})

    for link in bbc_links:
        if link.startswith('https://www.bbc.com/'):
            title, description = extract_article(link)
            articles.append({'title': title, 'description': description, 'source': 'BBC'})

    save_to_csv(articles, 'articles.csv')  # Use a relative path for the filename

# Define the DAG
dag = DAG(
    'mlops_a2',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',  # Run daily at 23:00
    catchup=False
)

# Define the main task using PythonOperator
main_task = PythonOperator(
    task_id='main',
    python_callable=main,
    dag=dag
)
