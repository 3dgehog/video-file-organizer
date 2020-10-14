FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install .

EXPOSE 5000

CMD [ "uwsgi", "--ini", "webserver.ini" ]