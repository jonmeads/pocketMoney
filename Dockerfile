FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron python3.7 python3-pip

COPY ./pocket /pocket
COPY ./requirements.txt requirements.txt 
COPY ./.flaskenv /.flaskenv

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5050
VOLUME /config
CMD flask run
