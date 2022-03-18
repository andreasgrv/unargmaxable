# Database management instructions
## How to install postgres locally without sudo: TL;DR;

First create the following environment variables:
- *DB_FOLDER:* The global path to the db folder, followed by the name of the folder you want the database files to be stored in.
- *DB_PORT:* The port on which we want access the postgres database.
- *DB_USER:* User to run db as - default to yourself.
- *DB_NAME:* What to call your db.
- *DB_PASSWD:* The password for database access.
- *PGPASSWORD:* Postgres uses this env variable for password.

``` bash
export DB_FOLDER="$PWD/stollen_data"
export DB_PORT=5436
export DB_USER=`whoami`
export DB_NAME=stollenprob
export DB_PASSWD="cov1d"
export PGPASSWORD=$DB_PASSWD
export DB_HOST="localhost"
export DB_SSL="prefer"
```

Run the *install.sh* script. The script relies on the above environment variables being set.
```
./install.sh
```
The script should exit gracefully, after which point the tables in the database as specified in our python code will have been created.
The tables are all created using flask-migrate: `flask db upgrade`.
NOTE: this script also starts the db, so there is no need to run *start.sh*.

- Caveat a) If anything goes wrong during installation, make sure you run *./stop.sh* before deleting any files. If you don't, you may be unable to delete files until you kill the postgres server.
- Caveat b) If *initdb* or *pg_ctl* commands are not found, you need to add them to your PATH. Something along the lines of:
```bash
export PATH="/usr/lib/postgresql/11/bin:$PATH"
```

## How to start / stop the database server

Use the available *start.sh* and *stop.sh* scripts.
