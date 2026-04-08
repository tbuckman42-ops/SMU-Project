FROM python:3.11

RUN apt-get update && apt-get install -y unixodbc-dev curl gnupg

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

WORKDIR /app

COPY . .

RUN pip install anvil-uplink pyodbc requests

CMD python anvil_uplink_copy.py
