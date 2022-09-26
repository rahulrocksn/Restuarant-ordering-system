ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DB_FILE=/data/db.sqlite3 \
    MEDIA_ROOT=/data/media \
    ENVIRONMENT=production
RUN python manage.py collectstatic --noinput


EXPOSE 8080

# replace APP_NAME with module name
CMD ["python", "manage.py", "runserver", "--insecure", "0.0.0.0:8080"]
#CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "chewsters.wsgi"]
