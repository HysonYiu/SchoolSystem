#!/data/data/com.termux/files/usr/bin/bash
# SchoolSystem Watchdog - auto restarts on crash
cd /data/data/com.termux/files/home/SchoolSystem
termux-wake-lock 2>/dev/null

echo "[$(date)] Watchdog started" >> log.txt

while true; do
    echo "[$(date)] Starting main.py..." >> log.txt
    python main.py >> log.txt 2>&1
    EXIT_CODE=$?
    echo "[$(date)] main.py exited with code $EXIT_CODE" >> log.txt
    
    # Check if restart was requested by update system
    if [ -f ".restart_requested" ]; then
        echo "[$(date)] Restart requested by update system" >> log.txt
        rm -f .restart_requested
        sleep 1
        continue
    fi
    
    # Normal crash - wait 3s and restart
    if [ $EXIT_CODE -ne 0 ]; then
        echo "[$(date)] Crashed! Restarting in 3s..." >> log.txt
        sleep 3
        continue
    fi
    
    # Clean exit (e.g. SIGTERM) - stop watchdog
    echo "[$(date)] Clean exit, stopping watchdog" >> log.txt
    break
done
