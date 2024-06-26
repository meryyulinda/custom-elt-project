FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client cron

COPY start.sh /app/start.sh
COPY elt_script.py .

WORKDIR /app

# Add the cron job
# This example runs the script every day at 18:55.
# Adjust the cron timing as needed.
RUN echo "55 18 * * * python /app/elt_script.py" | crontab -

CMD ["python", "elt_script.py"]