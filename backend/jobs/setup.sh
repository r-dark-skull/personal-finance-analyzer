#! /bin/bash

chmod +x /develop/jobs/script.py
mkdir -p /var/log/cron/
echo "Scheduling task" > /var/log/cron/jobs.log

echo '0 */8 * * * /develop/jobs/script.py >> /var/log/cron/jobs.log' | crontab -
service cron restart
