sudo iwconfig wlan0 mode managed essid off
sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
