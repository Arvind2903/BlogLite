#! /usr/bin/bash

python3 main.py &

# shellcheck disable=SC2164
cd frontend
npm run electron:serve &


wait




