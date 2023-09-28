FROM python:3.11.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN buildDeps='pkg-config build-essential' && \
    apt update && \
    apt install --no-install-recommends -y $buildDeps default-libmysqlclient-dev && \
    export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags` && \
    export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs` && \
    pip install mysqlclient && \
    apt purge -y --auto-remove $buildDeps && \
    rm -rf /var/cache/apt

ENV INSTALL_PATH /users_svc_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY ./requirements.txt $INSTALL_PATH
RUN pip install --no-cache-dir --requirement $INSTALL_PATH/requirements.txt

COPY . $INSTALL_PATH

CMD ["python3", "run.py"]

