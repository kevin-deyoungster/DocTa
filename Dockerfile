FROM python:3.7-slim

LABEL maintainer="Kevin de Youngster <kevin.deyoungster@gmail.com>"

COPY . /app

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev wget && \
    mkdir -p /installation/ && \
    wget https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb \
    --no-check-certificate \
    -O /installation/pandoc.deb && \
    dpkg -i /installation/pandoc.deb && \
    rm -rf /installation/ && \
    apt-get install -y tidy && \
    apt-get install -y texlive && \
    pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD ["docta.py"]