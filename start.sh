#!/bin/bash
pip install anvil-app-server anvil-uplink
python anvil_uplink_copy[1].py&
anvil-app-server --app Project
