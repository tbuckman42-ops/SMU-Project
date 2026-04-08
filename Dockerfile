FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install anvil-app-server anvil-uplink

EXPOSE 3030

CMD bash -c "python anvil_uplink_copy[1].py & anvil-app-server --app /app --port 3030 --origin https://smu-project-production.up.railway.app"
