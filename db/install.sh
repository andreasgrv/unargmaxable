#!/bin/bash
initdb -D $DB_FOLDER -A md5 -U $USER --pwfile=<(echo "$PGPASSWORD")
# Change the postgres.conf file port to 5434 and socket to /tmp
# 5434 worked for me
sed -i "s/#port = 5432/port = $DB_PORT/g" $DB_FOLDER/postgresql.conf
sed -i "s/#unix_socket_directories = /unix_socket_directories = '\/tmp' #/g" $DB_FOLDER/postgresql.conf
pg_ctl -D $DB_FOLDER -w start
# Create the database
createdb -p $DB_PORT -h /tmp $DB_NAME
# Create stollen user
psql -p $DB_PORT -h /tmp -d $DB_NAME -U $USER -c "CREATE ROLE stollen WITH LOGIN PASSWORD '$PGPASSWORD';"
# Give privileges
psql -p $DB_PORT -h /tmp -d $DB_NAME -U $USER -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to stollen;"
# Create tables and stuff
# We rely on flask migrations to deploy our database schema
# Our database schema is available in data_model.py
flask db init
flask db migrate -m 'Developer mode - ground zero'
flask db upgrade
