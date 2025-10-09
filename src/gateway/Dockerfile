FROM python:3.13.5-slim

ENV INSTALL_PATH=/gateway_svc_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY ./requirements.txt $INSTALL_PATH
RUN pip install --no-cache-dir --requirement $INSTALL_PATH/requirements.txt

COPY . $INSTALL_PATH

CMD ["python3", "run.py"]



