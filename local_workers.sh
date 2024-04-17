#! /usr/bin/bash

trap "kill 0" EXIT

sudo service redis-server start &

celery -A backend.celery beat --max-interval 1 -l info &

celery -A backend.celery worker -l info &

# shellcheck disable=SC2164
cd ~
./go/bin/MailHog &

wait
