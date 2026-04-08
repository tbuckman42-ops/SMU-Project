FROM python:3.11

RUN apt-get update && apt-get install -y default-jdk unixodbc-dev

WORKDIR /app

RUN pip install anvil-app-server anvil-uplink pyodbc

RUN anvil-app-server --get-source 2>/dev/null || true

RUN wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -O /usr/local/lib/postgresql.jar

COPY . .

EXPOSE 3030

CMD bash -c "python anvil_uplink_copy.py & anvil-app-server --app /app --port 3030 --origin https://smu-project-production.up.railway.app --database jdbc:postgresql://maglev.proxy.rlwy.net:11616/railway?user=postgres&password=xudmdAhBWjBbdSSTuWIOOkFpZdCHYskx"
