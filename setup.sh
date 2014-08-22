#!/bin/bash

function append {
    if [ -z "$( grep "$1" "$2" )"]; then
        echo $1 | sudo tee -a $2
    fi
}

cd ~

if [ -z "$(crontab -l | grep Alarm)" ]; then
	line="# 0 7 * * * sh /usr/local/bin/alarmcron.sh > ~/logs/cron/cron.txt # Alarm"
	(crontab -l; echo "$line" ) | crontab -
fi
if [ -z "$(crontab -l | grep "Check WiFi")" ]; then
	line="* * * * * sudo /usr/local/bin/check-wifi.sh # Check WiFi"
	(crontab -l; echo "$line" ) | crontab -
fi



sudo apt-get update
sudo apt-get install mpc python-dev python-rpi.gpio python-pip htop elinks evtest tslib libts-bin python-gtk2 xinput
sudo pip install python-crontab requests python-mpd2
mkdir logs
mkdir logs/cron


git clone https://github.com/Giannie/Pi_Time

mkdir tft

cd tft
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-bin-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-dev-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-doc-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi0-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/raspberrypi-bootloader-adafruit-20140724-1.deb
wget http://adafruit-download.s3.amazonaws.com/xinput-calibrator_0.7.5-1_armhf.deb
sudo dpkg -i -B *.deb

sudo mv /usr/share/X11/xorg.conf.d/99-fbturbo.conf ./

cd

append spi-bcm2708 /etc/modules
append fbtft_device /etc/modules
append rpi_power_switch /etc/modules

append "options fbtft_device name=adafruitts rotate=270 frequency=32000000" /etc/modprobe.d/adafruit.conf
append "options rpi_power_switch gpio_pin=23 mode=0" /etc/modprobe.d/adafruit.conf

append "SUBSYSTEM==\"input\", ATTRS{name}==\"stmpe-ts\", ENV{DEVNAME}==\"*event*\", SYMLINK+=\"input/touchscreen\""  /etc/udev/rules.d/95-stmpe.rules

if [ -z "$( grep "echo 252 > /sys/class/gpio/export" /etc/rc.local )" ]; then
    sudo sed -i s/'exit 0'/''/ /etc/rc.local
    append "echo 252 > /sys/class/gpio/export" /etc/rc.local
    append "echo 'out' > /sys/class/gpio/gpio252/direction" /etc/rc.local
    append "echo '1' > /sys/class/gpio/gpio252/value" /etc/rc.local
    append "DISPLAY=:0.0 python /home/pi/Pi_Time/Python/screen_control.py &" /etc/rc.local
    append "exit 0" /etc/rc.local
fi

if [ -z "$( grep "dpms -nocursor" /etc/lightdm/lightdm.conf )" ]; then
    sudo sed -i s/'#xserver-command=X'/'xserver-command=X -s 0 dpms -nocursor'/ /etc/lightdm/lightdm.conf
fi

if [ -z "$( grep python /etc/xdg/lxsession/LXDE/autostart )" ]; then
    sudo sed -i 's/^\([^#]\)/#\1/g' /etc/xdg/lxsession/LXDE/autostart
    echo "@python ~/Pi_Time/Python/alarm_gui.py" | sudo tee -a /etc/xdg/lxsession/LXDE/autostart
fi

cd Pi_Time
sudo cp usr\ local\ bin/* /usr/local/bin/
sudo cp 99-fbdev.conf /usr/share/X11/xorg.conf.d/


