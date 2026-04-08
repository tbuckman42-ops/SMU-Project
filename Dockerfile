FROM python:3.11

RUN apt-get update && apt-get install -y default-jdk unixodbc-dev wget

WORKDIR /app

COPY . .

RUN pip install anvil-app-server anvil-uplink pyodbc

EXPOSE 8080

CMD bash -c "python anvil_uplink_copy.py & anvil-app-server --app /app --port 8080 --auto-migrate --origin https://smu-project.onrender.com --database 'jdbc:postgresql://maglev.proxy.rlwy.net:11616/railway?user=postgres&password=xudmdAhBWjBbdSSTuWIOOkFpZdCHYskx&sslmode=require' --letsencrypt-storage /dev/null 2>&1"
