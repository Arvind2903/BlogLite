#! /usr/bin/bash

killall MailHog
killall celery
sudo service redis-server stop
# shellcheck disable=SC2046
kill -9 $(lsof -t -i:8080)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i:5000)
