FROM python:3.10-slim

# Tizim kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y gettext libpq-dev gcc

# Ishchi papkani yaratish
WORKDIR /app

# Python kutubxonalarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani ko'chirish
COPY . /app/

# Portlarni ochish
EXPOSE 8000 8080

# Default komanda (django va celery uchun ishlatiladi)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
