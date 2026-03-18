#!/data/data/com.termux/files/usr/bin/bash
# Termux:Boot - runs on phone boot
sleep 10  # wait for network
termux-wake-lock
sshd
cd /data/data/com.termux/files/home/SchoolSystem
nohup bash start.sh > /dev/null 2>&1 &
