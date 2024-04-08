#!/bin/bash

sudo ifconfig wlan0 up
wpa_cli terminate
sudo iwconfig wlan0 essid achraf mode ad-hoc channel 1 enc off
sudo ifconfig wlan0 up
sudo ifconfig wlan0 192.168.21.1 netmask 255.255.255.0 broadcast 192.168.21.0
