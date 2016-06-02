#!/usr/bin/env python
""" Main configuration file for application
"""

# wsjtx server
server_address = ('127.0.0.1', 2237)

# use curses interface
use_curses = True

# exit py_wsjtx on WSJT-X exit
exit_on_wsjtxexit = False

# show popup notifications
notify_alert = True

# publish messages to an MQTT server
# (requires paho library)
use_mqtt = True
mqtt_server = "192.168.0.12"

# write all decodes to a log file
log_decodes = False
log_outfile = "/tmp/py_wsjtx.log"

