#!/bin/bash

chmod +x phantomjs/bin/phantomjs
pip3 install --user python-crontab
is_reset=0
while getopts c opt
do
  case "$1" in
    -c)
    is_reset=1
  esac
  shift
done
if [ $is_reset == 1 ]
then
  python3 cron.py -c
else
  python3 cron.py
fi

