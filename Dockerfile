# To build: docker build -t 3pi-workflow:latest .
FROM ubuntu:latest

MAINTANER Jean Vicelli "jean.vicelli@digitalglobe.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# ENTRYPOINT [ "python" ]

CMD [ "run_pipeline.sh" ]