FROM python:3.10-alpine
EXPOSE 8000
WORKDIR /app

RUN apk add --no-cache gdal gdal-dev geos-dev libpq-dev postgresql-client
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app