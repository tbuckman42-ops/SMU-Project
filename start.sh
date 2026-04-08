#!/bin/bash
pip install anvil-app-server anvil-uplink
python anvil_uplink_copy.py&
anvil-app-server --app Project
