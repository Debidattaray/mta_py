#!/bin/bash

LOG_DIR=

truncate -s 0 /etc/pmta/log/pmta.log
truncate -s 0 /etc/pmta/log/pmta.log.1

(crontab -l | grep -q "/apps/clear_log.sh") || (crontab -l; echo "0 */4 * * * /apps/clear_log.sh") | crontab -