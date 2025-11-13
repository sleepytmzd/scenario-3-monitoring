#!/bin/bash

PROMETHEUS_URL="http://prometheus:9090/api/v1/alerts"
LOG_FILE="alerts.log"

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

curl -s $PROMETHEUS_URL | jq -r '.data.alerts[] | "\($labels.alertname) - \($annotations.summary) - \($status) - $TIMESTAMP"' >> $LOG_FILE

cat $LOG_FILE