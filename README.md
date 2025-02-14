# Apartment_sales
Apartment Sales Data Pipeline
This project is an ETL pipeline for collecting, processing, and storing real estate listings from ss.com. It uses Airflow for automation, PostgreSQL for data storage, and Docker for containerization.

Features:
✅ Web scraping of apartment listings using BeautifulSoup and requests
✅ Data storage in PostgreSQL with city and district reference tables
✅ Automated daily updates via Apache Airflow DAGs
✅ Containerized setup with Docker & Docker Compose

Tech Stack:
Python (requests, BeautifulSoup, pandas, psycopg2)
Apache Airflow for task scheduling
PostgreSQL for structured data storage
Docker for easy deployment
This project is designed for data engineers looking to practice ETL workflows, web scraping, and Airflow orchestration. 
