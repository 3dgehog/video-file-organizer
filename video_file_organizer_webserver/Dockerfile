FROM python:3.6

COPY . /app

WORKDIR /config

RUN mkdir -p /dirs

RUN pip install /app

EXPOSE 5000

CMD [ "uwsgi", "--ini", "/app/webserver.ini" ]