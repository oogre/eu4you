#!/bin/sh

#!/bin/sh

### BEGIN INIT INFO
# Provides:          start.eu4you.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start ~/Desktop/eu4you/start.py
# Description:
### END INIT INFO

PID=$(ps aux | grep -v grep | grep 'start.eu4you.py' | awk '{print $2}')
if [ -z "$PID" ]
then
	echo "START"
	cd ~/Desktop/eu4You/scripts/
	LOG_FILE=../eu4you.log
	touch "$LOG_FILE"
	python start.eu4you.py &
else
	echo "killing $PID"
	kill -15 $PID
fi