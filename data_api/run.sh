#!/bin/bash

#################################################################
#
# crontab scheduled jobs (crontab -e)
# path: /home/powerlim2/project_free_insight/data_api/run.sh
# time: 0 21 * * *
#
#################################################################


# create a temp file with suffix .crontab
TEMP_FILE=`mktemp --suffix .crontab`
touch $TEMP_FILE

# scheduled jobs:
/usr/bin/python /home/powerlim2/project_free_insight/data_api/run.py > /tmp/stock_retrieval.txt
echo "The scheduled jobs are finished successfully!" | mailx -v -A gmail -s "Project Free Insight: (Data API) Crontab Result" -a /tmp/stock_retrieval.txt powerlim2@gmail.com
rm /tmp/stock_retrieval.txt

# we are done, clean-up after ourselves
rm $TEMP_FILE