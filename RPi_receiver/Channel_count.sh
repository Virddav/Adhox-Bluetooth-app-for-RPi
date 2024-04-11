#!/bin/bash 

result=$(iwlist wlan0 scan)

channels=$(echo "$result" | grep "Channel:" | awk '{print $NF}' | sort | uniq -c | sort -n)

echo "Nombre d'occurences de chaque canal :"
echo "$channels"
