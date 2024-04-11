#!/bin/bash 
iwlist wlan0 channel > log_res
iwconfig wlan0 | grep "Bit Rate" >> log_res 
iwconfig wlan0 | grep "Link Quality" >> log_res
ifconfig wlan0 | grep "TX errors" >> log_res


