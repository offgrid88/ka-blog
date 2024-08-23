#!/bin/bash
echo "0 12 * * * /usr/bin/certbot renew --quiet" > /etc/cron.d/certbot
chmod 0644 /etc/cron.d/certbot
crontab /etc/cron.d/certbot
cron -f

