# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.6-slim

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y gconf-service wget libasound2 libgbm1 libappindicator3-1 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
# Allow statements and log messages to immediately appear in the Knative logs


USER root
ARG entity

COPY scraper_functions/$entity.py ./entity.py
COPY requirements.txt .
COPY chromedriver .
RUN pip install -r ./requirements.txt
RUN chmod +x ./entity.py



ENV AWS_ACCESS_KEY_ID='AKIA3DYWXELIXCXWBIUS'
ENV AWS_SECRET_ACCESS_KEY='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'

CMD [ "python3", "./entity.py" ]
