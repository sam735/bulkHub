#!/bin/bash
sudo /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf reread
sudo /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf update
sudo /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf stop bulkHub
sudo /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf start bulkHub