#!/bin/bash

if [ -z "$(echo $PATH | grep /usr/local/bin)" ]; then
    PATH=/usr/local/bin:$PATH
fi

python /home/pi/Pi_Time/Python/send_command.py on
#plug_on.sh && plug_on.sh &
python /home/pi/Pi_Time/Python/alarm_off.py
sudo sh -c "echo '1' > /sys/class/gpio/gpio252/value"
DISPLAY=:0.0 xinput set-prop 'stmpe-ts' 'Device Enabled' 1
mpc random on
mpc load AlarmPlaylist.m3u
mpc play
mpc pause
sleep 5
mpc volume 82
mpc play
mpc volume 80
sleep 15
mpc volume 82
sleep 15
mpc volume 84
sleep 15
mpc volume 86
sleep 15
mpc volume 88
sleep 15
mpc volume 90
string="$(mpc | grep playing)"
if [ -z "$string" ]
    then
        mpc load AlarmPlaylist.m3u
        mpc volume 80
        mpc play
        sleep 15
        mpc volume 82
        sleep 15
        mpc volume 84
        sleep 15
        mpc volume 86
        sleep 15
        mpc volume 88
        sleep 15
        mpc volume 90
fi
sleep 240
mpc volume 85
sleep 1560
string="$(mpc | grep playing)"
if [ "$string" ]; then
	mpc idle
	mpc pause
#	python /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/weather.py
	mpc play
fi
sleep 1800
string="$(mpc | grep playing)"
if [ "$string" ]; then
	mpc idle
fi
mpc random off
mpc stop
mpc clear
mpc volume 90
#plug_off.sh && plug_off.sh &
python /home/pi/Pi_Time/Python/send_command.py off
