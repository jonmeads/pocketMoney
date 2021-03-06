FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG ARG_TIMEZONE=Europe/London
ENV ENV_TIMEZONE ${ARG_TIMEZONE}

# install
RUN apt-get update && apt-get install -y cron python3.7 python3-pip tzdata 

# sync timezone
RUN echo '$ENV_TIMEZONE' > /etc/timezone \
    && ln -fsn /usr/share/zoneinfo/$ENV_TIMEZONE /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

# copy application
COPY ./pocket /pocket
COPY ./requirements.txt requirements.txt 
COPY ./.flaskenv .flaskenv
COPY ./payment.py payment.py 
COPY ./payment.sh payment.sh

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5050
VOLUME /config
CMD cron && flask run
