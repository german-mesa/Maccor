FROM python:3.8-slim

RUN pip install fastapi uvicorn pymacnet

WORKDIR /opt/fastapi

COPY ./fastapi_server/main.py /opt/fastapi

CMD [ "python" ,"./main.py"]
