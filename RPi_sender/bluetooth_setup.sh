#!/bin/bash
sudo bluetoothctl << EOF
agent on 
scan on
discoverable on 
pairable on
pair B8:27:EB:C9:02:3B
trust B8:27:EB:C9:02:3B
connect B8:27:EB:C9:02:3B
scan off
EOF
