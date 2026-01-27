FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

COPY cron/expire_counters.cron /etc/cron.d/expire_counters
RUN chmod 0644 /etc/cron.d/expire_counters
RUN crontab /etc/cron.d/expire_counters

RUN touch /var/log/cron.log

CMD cron && uvicorn main:app --host 0.0.0.0 --port 8001

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]