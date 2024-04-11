#!/bin/bash
sudo bluetoothctl << EOF
agent on 
scan on
discoverable on 
pairable on
pair B8:27:EB:C8:39:7F
trust B8:27:EB:C8:39:7F
connect B8:27:EB:C8:39:7F

EOF
