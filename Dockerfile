FROM python:3.6

COPY . /app

COPY supervisord.conf /etc/supervisord.conf 

WORKDIR /config

RUN mkdir -p /dirs

RUN pip install /app

EXPOSE 5000

CMD ["/usr/local/bin/supervisord"]