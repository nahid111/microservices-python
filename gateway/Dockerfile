FROM python:3.10.13-slim

ENV INSTALL_PATH /gateway_svc_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "run.py"]
