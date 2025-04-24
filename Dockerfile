FROM python:3.11

WORKDIR /app

COPY requirements.txt . 

RUN apt-get update && apt-get install -y netcat-openbsd && \
    pip install --no-cache-dir -r requirements.txt

COPY trackerapp /app

EXPOSE 8000
EXPOSE 5432
EXPOSE 6379

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]