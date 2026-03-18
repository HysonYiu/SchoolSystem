#!/data/data/com.termux/files/usr/bin/bash
# SchoolSystem Watchdog v2
# - Auto restarts on crash (3s cooldown)
# - Health ping every 60s
# - Kills zombie if port stuck
# - Logs all events

BASE="/data/data/com.termux/files/home/SchoolSystem"
PYTHON="/data/data/com.termux/files/usr/bin/python"
LOG="$BASE/log.txt"
PORT=8081
PING_INTERVAL=60
MAX_FAILS=3

cd "$BASE"
termux-wake-lock 2>/dev/null
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Started v2 — port $PORT, ping every ${PING_INTERVAL}s" >> "$LOG"

ping_fail=0
last_pid=0

while true; do
    # ── Start the server ──────────────────────────────────────────────────────
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Launching main.py..." >> "$LOG"
    python main.py >> "$LOG" 2>&1 &
    APP_PID=$!
    last_pid=$APP_PID
    ping_fail=0
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] PID=$APP_PID" >> "$LOG"

    # ── Monitor loop ──────────────────────────────────────────────────────────
    while true; do
        sleep "$PING_INTERVAL"

        # Check if process is still alive
        if ! kill -0 "$APP_PID" 2>/dev/null; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Process died (PID=$APP_PID)" >> "$LOG"
            break
        fi

        # Health ping
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
            --connect-timeout 5 --max-time 10 \
            "http://localhost:$PORT/health" 2>/dev/null)

        if [ "$HTTP_CODE" = "200" ]; then
            ping_fail=0
            # Check for restart request
            if [ -f "$BASE/.restart_requested" ]; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Restart requested" >> "$LOG"
                rm -f "$BASE/.restart_requested"
                kill "$APP_PID" 2>/dev/null
                sleep 1
                break
            fi
        else
            ping_fail=$((ping_fail + 1))
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] ⚠️ Ping failed ($ping_fail/$MAX_FAILS) HTTP=$HTTP_CODE" >> "$LOG"

            if [ "$ping_fail" -ge "$MAX_FAILS" ]; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] ❌ $MAX_FAILS failures — killing PID=$APP_PID" >> "$LOG"
                kill -9 "$APP_PID" 2>/dev/null

                # Kill any zombie on the port
                ZOMBIE=$(lsof -ti :"$PORT" 2>/dev/null)
                if [ -n "$ZOMBIE" ]; then
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Killing zombie PIDs: $ZOMBIE" >> "$LOG"
                    kill -9 $ZOMBIE 2>/dev/null
                fi
                sleep 2
                break
            fi
        fi
    done

    # ── Cooldown before restart ───────────────────────────────────────────────
    EXIT_CODE=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] Restarting in 3s..." >> "$LOG"
    sleep 3
done
