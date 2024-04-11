#!/bin/bash 

#Passer en mode adhoc (Parfois il faut lancer 3 fois)
sudo ifconfig wlan0 up 
echo passage en mode adhoc
sudo wpa_cli terminate
sudo iwconfig wlan0 essid achraf mode ad-hoc channel 1 enc off
sudo ifconfig wlan0 192.168.21.2 netmask 255.255.255.0 broadcast 192.168..00
iwconfig wlan0




