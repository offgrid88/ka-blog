#!/bin/sh
echo "Running my cron job at $(date)"
# Your additional commands here


0 12 * * * /usr/bin/certbot renew --quiet


