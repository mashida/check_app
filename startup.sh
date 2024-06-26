#!/bin/bash

# Run migrations
python manage.py migrate

#Update database from csv
python manage.py update_database_from_csv

# Add your cron job
echo "0 3 * * * /app/manage.py update_database_from_csv >> /var/log/cron.log 2>&1" | crontab -

# Start the cron daemon
cron -f &

# Run your main application command
exec "$@"

