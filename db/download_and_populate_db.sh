#!/bin/bash
echo "Downloading csv files containing data dump..."
echo "Saving files to data folder..."
mkdir -p data
wget https://stollen-experiments-data.s3.eu-west-1.amazonaws.com/models.csv.gz -O - | gunzip -c > data/models.csv
wget https://stollen-experiments-data.s3.eu-west-1.amazonaws.com/experiments.csv.gz -O - | gunzip -c > data/experiments.csv
wget https://stollen-experiments-data.s3.eu-west-1.amazonaws.com/results.csv.gz -O - | gunzip -c > data/results.csv

echo "Populating database..."
psql -p $DB_PORT -h /tmp -d $DB_NAME -U $USER  -c "\copy experiment FROM 'data/experiments.csv' delimiter ',' csv header"
psql -p $DB_PORT -h /tmp -d $DB_NAME -U $USER  -c "\copy model FROM 'data/models.csv' delimiter ',' csv header"
psql -p $DB_PORT -h /tmp -d $DB_NAME -U $USER  -c "\copy result FROM 'data/results.csv' delimiter ',' csv header"
