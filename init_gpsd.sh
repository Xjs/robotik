#!/bin/sh
stty -F /dev/ttyAMA0 38400
gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock

