FROM python:3.11

RUN apt-get update && apt-get install -y unixodbc-dev

WORKDIR /app

COPY . .

RUN pip install anvil-uplink pyodbc

CMD python anvil_uplink_copy.py
