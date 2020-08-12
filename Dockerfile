FROM python:3.8.5-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt --upgrade 

COPY . /app

EXPOSE 5000

