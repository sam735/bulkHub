#!/bin/bash
PROJECT_LOCATION=/home/ubuntu/bulkHub
#cp /home/ubuntu/.env $PROJECT_LOCATION/.env
#source $PROJECT_LOCATION/.env
#cd $PROJECT_LOCATION
#mkdir -p /home/ubuntu/logs
#sudo chown --recursive ubuntu: /home/ubuntu/logs
virtualenv -p python3 /home/ubuntu/bulkHub/env
sudo /home/ubuntu/bulkHub/env/bin/pip3 install -r /home/ubuntu/bulkHub/requirements.txt
chmod +x /home/ubuntu/bulkHub/start.sh