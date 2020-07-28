FROM python:3.7.8-slim-stretch

# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt --upgrade 

COPY . /app

EXPOSE 5000
# ENTRYPOINT ["flask"]
# CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]

