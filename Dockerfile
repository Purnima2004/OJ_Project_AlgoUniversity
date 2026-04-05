FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=oj_backend.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && rm -rf /var/lib/apt/lists/*

COPY oj_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY oj_backend/ .

RUN mkdir -p media static

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn oj_backend.wsgi:application --bind 0.0.0.0:8000"]
