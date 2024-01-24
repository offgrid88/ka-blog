FROM nginx:1.23-alpine
# Install cron
RUN apk --no-cache add dcron
# Copy the cron job script
COPY certbot.sh /etc/cron.d/certbot.sh

# Give execution rights on the cron job script
RUN chmod +x /etc/cron.d/certbot.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN apk add certbot certbot-nginx


RUN rm /etc/nginx/conf.d/default.conf



RUN touch /etc/cron.d/certbot.sh && echo "0 12 * * * /usr/bin/certbot.sh renew --quiet" > /etc/cron.d/certbot.sh 


