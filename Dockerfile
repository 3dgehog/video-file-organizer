FROM python:3.6

COPY . /app

WORKDIR /config

RUN apt install redis

RUN mkdir -p /dirs

RUN pip install /app

EXPOSE 5000

CMD ["/usr/bin/supervisord"]