FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install anvil-app-server anvil-uplink

CMD bash -c "python 'anvil_uplink_copy[1].py' & anvil-app-server --app Project"
