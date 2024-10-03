FROM python:3.12.5-slim

RUN apt update
RUN apt-get install -y python3-dev python3-psycopg2 gcc g++ musl-dev
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN apt-get install -y binutils gdal-bin libgdal-dev libgeos-dev libproj-dev postgresql-client
RUN rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_VERSION=3.3.2


WORKDIR /app
COPY --chown=python:python . /app


RUN chmod +x /app/entrypoints/server.sh
RUN chmod +x /app/entrypoints/worker.sh
RUN chmod +x /app/entrypoints/beat.sh
RUN chmod +x /app/entrypoints/daphne.sh
RUN chmod +x /app/entrypoints/dev.sh

RUN mkdir -p staticfiles && \
    chown -R python:python staticfiles

RUN pip install gdal==$(gdal-config --version)
COPY --chown=python:python ./requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt




EXPOSE 8000

CMD [ "/app/entrypoints/server.sh" ]
