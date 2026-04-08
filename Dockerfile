FROM python:3.11

RUN apt-get update && apt-get install -y default-jdk unixodbc-dev wget nginx

WORKDIR /app

COPY . .

RUN pip install anvil-app-server anvil-uplink pyodbc

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD bash -c "python anvil_uplink_copy.py & anvil-app-server --app /app --port 8081 --auto-migrate --origin https://smu-project.onrender.com --database 'jdbc:postgresql://maglev.proxy.rlwy.net:11616/railway?user=postgres&password=xudmdAhBWjBbdSSTuWIOOkFpZdCHYskx&sslmode=require' & nginx -g 'daemon off;' 2>&1"
