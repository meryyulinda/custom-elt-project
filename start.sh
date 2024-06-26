#!/bin/sh

# Start the cron daemon in the background
cron &

python /app/elt_script.py