#!/bin/bash

if [ -z "$(ifconfig wlan0 | grep "inet addr")" ]; then
	ifdown wlan0 && ifup —-force wlan0
fi

