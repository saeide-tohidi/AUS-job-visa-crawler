# AUS Job Visa Crawler

This project is aimed at crawling job visa information related to Australia. It collects data from the specified website and organizes it based on job visa IDs, titles, and associated jobs.

## Installation

To use this project, you need to install all the required libraries listed in the `requirements.txt` file. You can do this using the following command:

pip install -r requirements.txt



## Usage

### Running Celery Worker

To run the Celery worker for executing tasks, use the following command:

celery -A celery_app worker --loglevel=info


This command starts a Celery worker that listens for tasks to be executed.

### Running the Crawler Task

To run the crawler task, use the following command:

python run_crawler.py


This command executes the crawler task, which initiates the process of scraping job visa information from the specified website.

Make sure to configure any necessary settings or parameters in the respective files before running the commands.
