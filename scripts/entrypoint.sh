#!/usr/bin/env bash
airflow db init
airflow webserver
airflow users create -u admin -f Admin -l User -r Admin -e admin@example.com -p admin