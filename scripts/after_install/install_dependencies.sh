#!/bin/bash
PROJECT_LOCATION=/home/ubuntu/bulkHub
cp /home/ubuntu/.env $PROJECT_LOCATION/.env
source $PROJECT_LOCATION/.env
cd $PROJECT_LOCATION
mkdir -p /home/ubuntu/logs
sudo chown --recursive ubuntu: /home/ubuntu/logs
virtualenv -p python3 env
source $PROJECT_LOCATION/env/bin/activate
pip3 install -r $PROJECT_LOCATION/requirements.txt
chmod +x $PROJECT_LOCATION/start.sh
deactivate