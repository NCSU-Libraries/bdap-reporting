FROM python:3.12.0a4-bullseye
COPY . /src
RUN pip install beautifulsoup4 lxml
WORKDIR /src