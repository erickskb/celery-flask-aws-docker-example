# To build: docker build -t 3pi-workflow:latest .
# To run: docker run -d -p 8000:8000 3pi-workflow
# To test: http://localhost:8000/status
FROM ubuntu:latest

MAINTAINER Jean Vicelli "jean.vicelli@digitalglobe.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libssl-dev libcurl4-openssl-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /app

# ENTRYPOINT [ "python" ]

EXPOSE 8000

RUN chmod +x run_pipeline.sh
CMD [ "./run_pipeline.sh" ]
