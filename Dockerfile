FROM python:3.11

RUN apt-get update && apt-get install -y default-jdk unixodbc-dev

WORKDIR /app

COPY . .

RUN pip install anvil-app-server anvil-uplink pyodbc

EXPOSE 3030

CMD bash -c "python anvil_uplink_copy.py & anvil-app-server --app /app --port 3030 --origin https://smu-project-production.up.railway.app --database none"
