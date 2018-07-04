FROM python:2.7-slim

WORKDIR /app

ADD . /app

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y pandoc && \
    apt-get install -y tidy && \
    pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV NAME World

CMD ["python","docta.py"]

