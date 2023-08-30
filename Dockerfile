FROM python:3
COPY . /src
RUN pip install beautifulsoup4 lxml
WORKDIR /src