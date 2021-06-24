#!/bin/bash
PROJECT_LOCATION=/home/ubuntu/bulkHub
# cp /home/ubuntu/.env $PROJECT_LOCATION/.env
# source $PROJECT_LOCATION/.env
cd $PROJECT_LOCATION
#mkdir -p /home/ubuntu/logs
#sudo chown --recursive ubuntu: /home/ubuntu/logs
virtualenv -p python3 env
source /env/bin/activate
pip3 install -r requirements.txt
chmod +x start.sh
deactivate