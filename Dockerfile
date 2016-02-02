FROM python:2.7
RUN apt-get install -y curl
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN curl -LO https://github.com/daivq/VNWcrawl/archive/vnw.tar.gz
RUN tar xzf vnw.tar.gz

WORKDIR /usr/src/app/VNWcrawl-vnw/vnw
RUN pip install --no-cache-dir -r requirements.txt
