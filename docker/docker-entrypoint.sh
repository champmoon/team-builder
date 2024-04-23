#!/bin/sh
 
set -e
 
# Activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

export PYTHONPATH=.

# Run pre_start script: check health for db
python app/scripts/pre_start/check_health.py

# Run migrations
# alembic revision --autogenerate -m 'create_tables'
alembic upgrade head

# Run scripts to fill db
python app/scripts/pre_start/first_admin.py
python app/scripts/pre_start/exercises_types.py
python app/scripts/pre_start/workouts_statuses.py

sh -c "$*"
