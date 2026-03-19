#!/data/data/com.termux/files/usr/bin/bash
# SchoolSystem Watchdog v3 — Self-updating
# After admin update, watchdog re-execs itself to pick up new version

BASE="/data/data/com.termux/files/home/SchoolSystem"
PYTHON="/data/data/com.termux/files/usr/bin/python"
LOG="$BASE/log.txt"
PORT=8081
PING_INTERVAL=60
MAX_FAILS=3
SELF="$BASE/start.sh"
SELF_HASH=""

cd "$BASE"
termux-wake-lock 2>/dev/null

_log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] $*" >> "$LOG"; }
_log "Started v3 (PID=$$) — port $PORT, ping every ${PING_INTERVAL}s"

# Record own hash for self-update detection
SELF_HASH=$(md5sum "$SELF" 2>/dev/null | cut -d' ' -f1)

while true; do
    # ── Check if start.sh itself was updated ─────────────────────────────────
    NEW_HASH=$(md5sum "$SELF" 2>/dev/null | cut -d' ' -f1)
    if [ -n "$NEW_HASH" ] && [ "$NEW_HASH" != "$SELF_HASH" ]; then
        _log "start.sh updated (hash changed) — re-exec watchdog"
        chmod +x "$SELF"
        exec bash "$SELF"
        exit 0
    fi

    # ── Launch main.py ───────────────────────────────────────────────────────
    _log "Launching main.py..."
    python main.py >> "$LOG" 2>&1 &
    APP_PID=$!
    PING_FAIL=0
    _log "PID=$APP_PID"

    # ── Monitor loop ─────────────────────────────────────────────────────────
    while true; do
        sleep "$PING_INTERVAL"

        # Process alive check
        if ! kill -0 "$APP_PID" 2>/dev/null; then
            _log "Process died (PID=$APP_PID) — restarting"
            break
        fi

        # Restart request from admin update
        if [ -f "$BASE/.restart_requested" ]; then
            _log "Restart requested by admin update"
            rm -f "$BASE/.restart_requested"
            kill "$APP_PID" 2>/dev/null
            sleep 1
            break
        fi

        # Health ping
        HTTP=$(curl -s -o /dev/null -w "%{http_code}" \
            --connect-timeout 5 --max-time 10 \
            "http://localhost:$PORT/health" 2>/dev/null)

        if [ "$HTTP" = "200" ]; then
            PING_FAIL=0
        else
            PING_FAIL=$((PING_FAIL + 1))
            _log "⚠️ Ping failed ($PING_FAIL/$MAX_FAILS) HTTP=$HTTP"
            if [ "$PING_FAIL" -ge "$MAX_FAILS" ]; then
                _log "❌ Max failures — killing PID=$APP_PID"
                kill -9 "$APP_PID" 2>/dev/null
                # Kill zombie on port
                ZOMBIE=$(lsof -ti :"$PORT" 2>/dev/null)
                [ -n "$ZOMBIE" ] && kill -9 $ZOMBIE 2>/dev/null && _log "Killed zombie: $ZOMBIE"
                sleep 2
                break
            fi
        fi
    done

    _log "Cooldown 3s before restart..."
    sleep 3
done
