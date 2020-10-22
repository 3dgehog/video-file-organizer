FROM python:3.6

COPY . /app

WORKDIR /config

RUN mkdir -p /dirs

RUN pip install /app

CMD [ "vfo", "--scheduler" ]