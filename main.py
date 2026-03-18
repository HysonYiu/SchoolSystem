import os, sqlite3, threading, time, sys, json, shutil
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, g, Response, make_response, redirect
from dotenv import load_dotenv

load_dotenv()
__version__ = "2.0.0-alpha.1"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB for audio uploads

SECRET_KEY   = os.getenv("SECRET_KEY", "changeme")
ADMIN_KEY    = os.getenv("ADMIN_KEY", "adminme")
DB_PATH      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schoolsystem.db")
ENV_PATH     = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

try:
    PORT = int(os.getenv("PORT", "8081"))
except ValueError:
    PORT = 8081
HOST         = os.getenv("BIND_HOST", "0.0.0.0")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GH_REPO      = os.getenv("GITHUB_REPO", "SchoolSystemYiu/SchoolSystem")
GH_TOKEN     = os.getenv("GITHUB_TOKEN", "")

from recording import recording_bp
app.register_blueprint(recording_bp)


# ── DB ────────────────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS homeworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, subject TEXT NOT NULL,
        hw_type TEXT DEFAULT '功課', due_date TEXT, due_day INTEGER,
        priority TEXT DEFAULT '中', notes TEXT DEFAULT '',
        source TEXT DEFAULT '手動', done INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL, title TEXT,
        exam_date TEXT NOT NULL, scope TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT, minutes INTEGER DEFAULT 0,
        session_date TEXT DEFAULT (date('now','localtime')), notes TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS access_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT, action TEXT, detail TEXT,
        ts TEXT DEFAULT (datetime('now','localtime'))
    );
    """)
    db.commit(); db.close()
    print(f"[DB] {DB_PATH}")


# ── Auth ──────────────────────────────────────────────────────────────────────

def auth(req):
    k = req.args.get("key") or req.headers.get("X-API-Key") or req.cookies.get("key")
    return k == SECRET_KEY

def admin_auth(req):
    k = req.args.get("admin") or req.headers.get("X-Admin-Key") or req.cookies.get("admin")
    return k == ADMIN_KEY

def log_action(action, detail=""):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute("INSERT INTO access_log(ip,action,detail) VALUES(?,?,?)",
                   (request.remote_addr, action, detail))
        db.commit(); db.close()
    except Exception as e:
        pass


# ── Cycle helpers ─────────────────────────────────────────────────────────────

def _get_cycle_and_school():
    from timetable import get_cycle_day, is_school_day, get_next_school_day
    return get_cycle_day, is_school_day, get_next_school_day


# ── Web pages ─────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status":"ok","version":__version__,"ts":datetime.now().isoformat()})

@app.route("/")
def index():
    if not auth(request): return redirect("/login")
    from ui import UI_HTML
    html = UI_HTML.replace("KEY_PLACEHOLDER", SECRET_KEY)
    resp = make_response(Response(html, mimetype="text/html"))
    resp.set_cookie("key", SECRET_KEY, max_age=30*24*3600)
    return resp

@app.route("/login", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        k = request.form.get("key","")
        if k == SECRET_KEY:
            resp = make_response(redirect("/"))
            resp.set_cookie("key", k, max_age=30*24*3600)
            return resp
        error = "密鑰錯誤，請重試"
    return f"""<!DOCTYPE html><html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>SchoolSystem</title></head>
<body style="margin:0;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;min-height:100vh">
<div style="width:100%;max-width:360px;padding:40px 24px;text-align:center">
<div style="font-size:52px;margin-bottom:16px">📚</div>
<div style="font-size:28px;font-weight:700;letter-spacing:-1px;margin-bottom:6px">SchoolSystem</div>
<div style="font-size:13px;color:#636366;margin-bottom:40px">v{__version__}</div>
{"" if not error else f'<div style="background:rgba(255,59,48,.15);color:#ff453a;padding:10px 16px;border-radius:10px;font-size:14px;margin-bottom:16px">{error}</div>'}
<form method="post" action="/login">
<input name="key" type="password" placeholder="輸入密鑰" autofocus
  style="width:100%;background:#1c1c1e;border:none;color:#fff;padding:15px 16px;border-radius:14px;font-size:16px;margin-bottom:12px;font-family:inherit;outline:none;-webkit-appearance:none">
<button type="submit"
  style="width:100%;background:#0a84ff;color:#fff;border:none;padding:15px;border-radius:14px;font-size:17px;font-weight:600;cursor:pointer;font-family:inherit">
  登入
</button>
</form>
</div></body></html>"""

@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.delete_cookie("key"); resp.delete_cookie("admin")
    return resp


# ── Homework ──────────────────────────────────────────────────────────────────

PRIORITY_ORDER = "CASE priority WHEN '高' THEN 1 WHEN '中' THEN 2 WHEN '低' THEN 3 ELSE 4 END"

@app.route("/api/hw", methods=["GET"])
def hw_list():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    try:
        done = int(request.args.get("done","0"))
    except ValueError:
        done = 0
    subj = request.args.get("subject","")
    q = "SELECT * FROM homeworks WHERE done=?"
    p = [done]
    if subj: q += " AND subject=?"; p.append(subj)
    q += f" ORDER BY due_date ASC, {PRIORITY_ORDER}"
    return jsonify([dict(r) for r in db.execute(q,p).fetchall()])

@app.route("/api/hw", methods=["POST"])
def hw_add():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    d = request.get_json()
    if not d or not d.get("title") or not d.get("subject"):
        return jsonify({"error":"title and subject required"}),400
    db = get_db()
    db.execute("INSERT INTO homeworks(title,subject,hw_type,due_date,due_day,priority,notes,source) VALUES(?,?,?,?,?,?,?,?)",
        (d["title"],d["subject"],d.get("hw_type","功課"),d.get("due_date",""),
         d.get("due_day"),d.get("priority","中"),d.get("notes",""),d.get("source","手動")))
    db.commit()
    log_action("hw_add", d["title"])
    return jsonify({"ok":True})

@app.route("/api/hw/<int:hw_id>/done", methods=["POST"])
def hw_done(hw_id):
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    db.execute("UPDATE homeworks SET done=1 WHERE id=?", (hw_id,))
    db.commit()
    log_action("hw_done", str(hw_id))
    return jsonify({"ok":True})

@app.route("/api/hw/<int:hw_id>/undone", methods=["POST"])
def hw_undone(hw_id):
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    db.execute("UPDATE homeworks SET done=0 WHERE id=?", (hw_id,))
    db.commit()
    log_action("hw_undone", str(hw_id))
    return jsonify({"ok":True})

@app.route("/api/hw/<int:hw_id>", methods=["DELETE"])
def hw_delete(hw_id):
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    db.execute("DELETE FROM homeworks WHERE id=?", (hw_id,))
    db.commit()
    return jsonify({"ok":True})

@app.route("/api/today")
def today():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    today_str = date.today().isoformat()
    hw = db.execute("SELECT * FROM homeworks WHERE done=0 AND due_date!='' AND due_date<=? ORDER BY due_date ASC",(today_str,)).fetchall()
    exams = db.execute("SELECT * FROM exams WHERE exam_date>=? ORDER BY exam_date ASC LIMIT 5",(today_str,)).fetchall()
    get_cycle_day, is_school_day, _ = _get_cycle_and_school()
    return jsonify({
        "date": today_str,
        "cycle_day": get_cycle_day(),
        "is_school_day": is_school_day(),
        "overdue_and_today": [dict(r) for r in hw],
        "upcoming_exams": [dict(r) for r in exams]
    })


# ── Timetable ─────────────────────────────────────────────────────────────────

@app.route("/api/timetable")
def timetable():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    from timetable import TIMETABLE
    day = request.args.get("day")
    if day:
        slots = TIMETABLE.get(int(day),[])
        return jsonify({"day":int(day),"slots":[{"start":s[0],"end":s[1],"subject":s[2],"room":s[3]} for s in slots]})
    result = {}
    for d,slots in TIMETABLE.items():
        result[str(d)] = [{"start":s[0],"end":s[1],"subject":s[2],"room":s[3]} for s in slots]
    return jsonify(result)

@app.route("/api/cycle")
def cycle():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    get_cycle_day, is_school_day, get_next_school_day = _get_cycle_and_school()
    today_date = date.today()
    day_num = get_cycle_day(today_date)
    school  = is_school_day(today_date)
    next_d  = get_next_school_day(today_date)
    next_day_num = get_cycle_day(next_d)
    return jsonify({
        "today": today_date.isoformat(),
        "is_school_day": school,
        "cycle_day": day_num,
        "next_school_date": next_d.isoformat(),
        "next_cycle_day": next_day_num,
    })


# ── Exams ─────────────────────────────────────────────────────────────────────

@app.route("/api/exams", methods=["GET"])
def exam_list():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    rows = db.execute("SELECT *, julianday(exam_date)-julianday('now') as days_left FROM exams ORDER BY exam_date ASC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/exams", methods=["POST"])
def exam_add():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    d = request.get_json()
    if not d or not d.get("subject") or not d.get("exam_date"):
        return jsonify({"error":"required"}),400
    db = get_db()
    db.execute("INSERT INTO exams(subject,title,exam_date,scope) VALUES(?,?,?,?)",
               (d["subject"],d.get("title",""),d["exam_date"],d.get("scope","")))
    db.commit()
    return jsonify({"ok":True})

@app.route("/api/exams/<int:ex_id>", methods=["DELETE"])
def exam_delete(ex_id):
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    db.execute("DELETE FROM exams WHERE id=?", (ex_id,))
    db.commit()
    return jsonify({"ok":True})


# ── Stats ─────────────────────────────────────────────────────────────────────

@app.route("/api/stats")
def stats():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    total   = db.execute("SELECT COUNT(*) FROM homeworks").fetchone()[0]
    done    = db.execute("SELECT COUNT(*) FROM homeworks WHERE done=1").fetchone()[0]
    overdue = db.execute("SELECT COUNT(*) FROM homeworks WHERE done=0 AND due_date!='' AND due_date<date('now','localtime')").fetchone()[0]
    by_subj = db.execute("SELECT subject,COUNT(*) as cnt FROM homeworks WHERE done=0 GROUP BY subject ORDER BY cnt DESC").fetchall()
    return jsonify({"total":total,"done":done,"pending":total-done,"overdue":overdue,"by_subject":[dict(r) for r in by_subj]})


# ── AI ────────────────────────────────────────────────────────────────────────

@app.route("/api/ai/ask", methods=["POST"])
def ai_ask():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    if not DEEPSEEK_KEY:
        return jsonify({"error":"no_key","msg":"請先設定 DEEPSEEK_API_KEY"}),503
    d = request.get_json()
    q = (d or {}).get("question","")
    if not q: return jsonify({"error":"empty"}),400
    db = get_db()
    hw    = db.execute("SELECT title,subject,due_date,priority FROM homeworks WHERE done=0 ORDER BY due_date ASC LIMIT 20").fetchall()
    exams = db.execute("SELECT subject,title,exam_date FROM exams WHERE exam_date>=date('now') ORDER BY exam_date ASC LIMIT 5").fetchall()
    get_cycle_day, _, _ = _get_cycle_and_school()
    ctx = f"今日 {date.today().isoformat()}，Cycle Day {get_cycle_day()}。未完成功課：{[dict(h) for h in hw]}。考試：{[dict(e) for e in exams]}。"
    try:
        import urllib.request as urlreq
        payload = json.dumps({"model":"deepseek-reasoner","max_tokens":800,"messages":[
            {"role":"system","content":"你係香港中學生學習助手，熟悉 DSE。用廣東話回答，簡潔清晰。背景："+ctx},
            {"role":"user","content":q}
        ]}).encode()
        req = urlreq.Request("https://api.deepseek.com/chat/completions", data=payload,
            headers={"Content-Type":"application/json","Authorization":f"Bearer {DEEPSEEK_KEY}"}, method="POST")
        with urlreq.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
        return jsonify({"ok":True,"answer":result["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/ai/study_plan", methods=["POST"])
def ai_study_plan():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    if not DEEPSEEK_KEY: return jsonify({"error":"no_key","msg":"請在管理員介面設定 DEEPSEEK_API_KEY"}),503
    d = request.get_json() or {}
    try:
        focus_days = int(d.get("days", 3))
    except (ValueError, TypeError):
        focus_days = 3
    try:
        from study_plan import generate_study_plan
        result = generate_study_plan(focus_days=focus_days)
        if result.get("error") == "no_key":
            return jsonify({"error":"no_key"}),503
        if result.get("error"):
            return jsonify({"error":result["error"]}),500
        return jsonify({"ok":True,"plan":result["plan"],"context":result.get("context",{})})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/api/study/priorities")
def study_priorities():
    """今日優先事項 (不用 AI Key)"""
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    try:
        from study_plan import get_today_priorities
        return jsonify(get_today_priorities())
    except Exception as e:
        return jsonify({"error":str(e)}),500

# ── Logs ──────────────────────────────────────────────────────────────────────

@app.route("/api/logs")
def logs():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    try:
        n = int(request.args.get("n",50))
        n = min(max(n, 1), 1000)  # Bounds: 1-1000
    except ValueError:
        n = 50
    rows = db.execute("SELECT * FROM access_log ORDER BY id DESC LIMIT ?",(n,)).fetchall()
    return jsonify([dict(r) for r in rows])


# ── Admin page ────────────────────────────────────────────────────────────────

ADMIN_HTML = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin — SchoolSystem</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;background:#000;color:#fff;padding:20px;min-height:100vh}
a{color:#0a84ff;text-decoration:none;font-size:14px}
h1{font-size:22px;font-weight:700;letter-spacing:-.8px;margin:16px 0 4px}
.sub{color:#636366;font-size:13px;margin-bottom:24px}
.card{background:#1c1c1e;border-radius:14px;padding:20px;margin-bottom:14px;border:1px solid rgba(255,255,255,0.07)}
.ct{font-size:11px;font-weight:600;color:#636366;text-transform:uppercase;letter-spacing:.7px;margin-bottom:12px}
.row{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:.5px solid rgba(255,255,255,0.06)}
.row:last-child{border-bottom:none}
.rl{font-size:14px;color:#aeaeb2}
.rv{font-size:14px;font-weight:500}
.btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.btn{padding:9px 16px;border-radius:10px;border:none;cursor:pointer;font-size:13px;font-weight:600;font-family:inherit;transition:opacity .15s}
.btn:active{opacity:.7}
.b-blue{background:#0a84ff;color:#fff}
.b-grn{background:rgba(52,199,89,.2);color:#30d158}
.b-red{background:rgba(255,59,48,.2);color:#ff453a}
.b-gray{background:#2c2c2e;color:#aeaeb2}
.tag{display:inline-block;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600}
.tok{background:rgba(52,199,89,.2);color:#30d158}
.twn{background:rgba(255,159,10,.2);color:#ff9f0a}
textarea{width:100%;background:#2c2c2e;border:1px solid rgba(255,255,255,.1);color:#fff;padding:14px;border-radius:10px;font-size:12px;font-family:'SF Mono',monospace;line-height:1.6;outline:none;resize:vertical}
#msg{padding:10px 14px;border-radius:10px;font-size:13px;margin-top:10px;display:none}
#msg.ok{background:rgba(52,199,89,.2);color:#30d158;display:block}
#msg.err{background:rgba(255,59,48,.2);color:#ff453a;display:block}
#umsg{font-size:13px;color:#636366;margin-top:10px;min-height:20px}
.log-box{background:#0a0a0a;border:1px solid #2c2c2e;border-radius:10px;padding:14px;font-size:12px;font-family:'SF Mono',monospace;line-height:1.8;max-height:400px;overflow-y:auto;white-space:pre-wrap;word-break:break-all;margin-top:10px}
.log-line.err{color:#ff453a}
.log-line.warn{color:#ff9f0a}
.log-line.ok{color:#30d158}
.log-line.info{color:#aeaeb2}
.seg{display:flex;background:#2c2c2e;border-radius:8px;padding:2px;margin-bottom:14px}
.seg-b{flex:1;padding:7px 4px;border:none;background:none;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer;color:#636366;font-family:inherit;transition:all .2s}
.seg-b.on{background:#3a3a3c;color:#fff}
.section{display:none}.section.on{display:block}
</style></head>
<body>
<a href="/?key=%%KEY%%">← 返回主頁</a>
<h1>⚙️ 管理員</h1>
<div class="sub">SchoolSystem v%%VER%%</div>

<div class="seg">
  <button class="seg-b on" onclick="switchTab('status',this)">狀態</button>
  <button class="seg-b" onclick="switchTab('update',this)">更新</button>
  <button class="seg-b" onclick="switchTab('logs',this)">日誌</button>
  <button class="seg-b" onclick="switchTab('config',this)">設定</button>
</div>

<!-- STATUS TAB -->
<div class="section on" id="t-status">
  <div class="card">
    <div class="ct">系統狀態</div>
    <div class="row"><span class="rl">版本</span><span class="rv" id="ver-disp">v%%VER%%</span></div>
    <div class="row"><span class="rl">今日 Cycle Day</span><span class="rv" id="cycle-disp">載入中...</span></div>
    <div class="row"><span class="rl">服務</span><span class="tag tok" id="svc-status">運行中</span></div>
    <div class="row"><span class="rl">端口</span><span class="rv">%%PORT%%</span></div>
    <div class="row"><span class="rl">數據庫</span><span class="rv" id="db-sz">-</span></div>
    <div class="row"><span class="rl">錄音資料夾</span><span class="rv" id="rec-sz">-</span></div>
    <div class="row"><span class="rl">待做功課</span><span class="rv" id="hw-cnt">-</span></div>
    <div class="row"><span class="rl">即將考試</span><span class="rv" id="ex-cnt">-</span></div>
  </div>
  <div class="card">
    <div class="ct">快速操作</div>
    <div class="btns">
      <button class="btn b-gray" onclick="doRst()">🔄 重啟服務</button>
      <button class="btn b-red" onclick="doRollback()">↩️ 回滾版本</button>
    </div>
    <div id="quick-msg" style="font-size:13px;color:#636366;margin-top:10px;min-height:18px"></div>
  </div>
</div>

<!-- UPDATE TAB -->
<div class="section" id="t-update">
  <div class="card">
    <div class="ct">GitHub 更新</div>
    <div class="row"><span class="rl">Repo</span><a href="https://github.com/%%REPO%%" target="_blank">%%REPO%% ↗</a></div>
    <div class="row"><span class="rl">本地版本</span><span class="rv">v%%VER%%</span></div>
    <div class="row"><span class="rl">遠端版本</span><span class="rv" id="rv">-</span></div>
    <div class="row"><span class="rl">更新狀態</span><span class="rv" id="upd-status">-</span></div>
    <div class="btns">
      <button class="btn b-blue" onclick="chkUpd()">🔍 檢查更新</button>
      <button class="btn b-grn" id="do-upd-btn" onclick="doUpd()" style="display:none">⬇️ 立即更新</button>
    </div>
    <div id="umsg"></div>
    <div id="upd-detail" style="display:none;margin-top:12px;font-size:12px;color:#636366"></div>
  </div>
</div>

<!-- LOGS TAB -->
<div class="section" id="t-logs">
  <div class="card">
    <div class="ct">系統日誌</div>
    <div class="btns">
      <button class="btn b-gray" onclick="loadLogs()">🔄 刷新</button>
      <button class="btn b-gray" onclick="loadFileLogs()">📄 查看 log.txt</button>
      <button class="btn b-red" onclick="clrLog()">🗑️ 清除日誌</button>
    </div>
    <div class="log-box" id="log-box">撳「刷新」載入日誌...</div>
  </div>
</div>

<!-- CONFIG TAB -->
<div class="section" id="t-config">
  <div class="card">
    <div class="ct">在線設定 (.env)</div>
    <div style="font-size:12px;color:#636366;margin-bottom:8px">⚠️ 修改後需要重啟才生效</div>
    <textarea id="env-ta" spellcheck="false" style="min-height:280px"></textarea>
    <div class="btns" style="margin-top:10px">
      <button class="btn b-blue" onclick="saveEnv()">💾 儲存</button>
      <button class="btn b-gray" onclick="loadEnv()">↺ 還原</button>
    </div>
    <div id="msg"></div>
  </div>
</div>

<script>
const A='%%ADMIN%%',K='%%KEY%%';
const adm=(p,o={})=>fetch(p+(p.includes('?')?'&':'?')+'admin='+A,{...o}).then(r=>r.json()).catch(e=>({error:e.message}));
const kap=(p,o={})=>fetch(p+(p.includes('?')?'&':'?')+'key='+K,{...o}).then(r=>r.json()).catch(e=>({error:e.message}));

function switchTab(t,el){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on'));
  document.querySelectorAll('.seg-b').forEach(b=>b.classList.remove('on'));
  document.getElementById('t-'+t).classList.add('on');
  el.classList.add('on');
  if(t==='logs')loadLogs();
  if(t==='config')loadEnv();
}

async function init(){
  const[c,s,sz,exams]=await Promise.all([
    kap('/api/cycle'),kap('/api/stats'),
    adm('/admin/dbsize'),kap('/api/exams')
  ]);
  document.getElementById('cycle-disp').textContent=c.is_school_day?'Day '+c.cycle_day:( c.error?'無法獲取':'假期');
  document.getElementById('hw-cnt').textContent=(s.pending||0)+' 項待做，'+(s.overdue||0)+' 項逾期';
  document.getElementById('ex-cnt').textContent=Array.isArray(exams)?exams.length+' 個':'-';
  document.getElementById('db-sz').textContent=(sz.db_kb||0)+' KB';
  document.getElementById('rec-sz').textContent=(sz.rec_kb||0)+' KB';
}

async function chkUpd(){
  const u=document.getElementById('umsg');
  const us=document.getElementById('upd-status');
  u.textContent='🔍 檢查中...';us.textContent='-';
  const r=await adm('/admin/check_update');
  const rv=document.getElementById('rv');
  rv.textContent=r.remote_version||( r.error?'❌ 錯誤':'-');
  if(r.has_update){
    us.textContent='🆕 有新版本！';
    u.textContent='發現新版本 '+r.remote_version+'，撳「立即更新」';
    document.getElementById('do-upd-btn').style.display='';
  }else if(r.error){
    us.textContent='❌ 檢查失敗';
    u.textContent='❌ '+r.error;
  }else{
    us.textContent='✅ 已是最新';
    u.textContent='✅ 已是最新版本';
    document.getElementById('do-upd-btn').style.display='none';
  }
}

async function doUpd(){
  if(!confirm('確定從 GitHub 下載最新版本並重啟？'))return;
  const u=document.getElementById('umsg');
  const det=document.getElementById('upd-detail');
  u.textContent='⬇️ 下載中...';det.style.display='none';
  const r=await adm('/admin/update');
  if(r.ok){
    u.textContent='✅ 更新成功！'+( r.updated?'已更新：'+r.updated.join(', '):'');
    if(r.errors&&r.errors.length){
      det.style.display='';det.textContent='部分失敗：'+r.errors.join('\n');
    }
    setTimeout(()=>{u.textContent='重啟中，5秒後刷新...';setTimeout(()=>location.reload(),5000);},1000);
  }else{
    u.textContent='❌ 更新失敗：'+(r.error||JSON.stringify(r));
  }
}

async function doRst(){
  if(!confirm('確定重啟？'))return;
  const m=document.getElementById('quick-msg');m.textContent='重啟中...';
  await adm('/admin/restart');
  m.textContent='重啟中，4秒後刷新...';
  setTimeout(()=>location.reload(),4000);
}

async function doRollback(){
  if(!confirm('回滾到上一個備份版本？'))return;
  const m=document.getElementById('quick-msg');m.textContent='回滾中...';
  const r=await adm('/admin/rollback');
  m.textContent=r.ok?'✅ 回滾成功，重啟中...':'❌ '+(r.error||'');
  if(r.ok)setTimeout(()=>location.reload(),4000);
}

async function loadLogs(){
  const box=document.getElementById('log-box');
  box.textContent='載入中...';
  const r=await kap('/api/logs?n=100');
  if(!Array.isArray(r)||!r.length){box.textContent='暫無日誌記錄';return;}
  box.innerHTML=r.map(l=>{
    const cls=l.action&&l.action.includes('error')?'err':l.action&&l.action.includes('ok')?'ok':'info';
    return'<div class="log-line '+cls+'">'+l.ts+' ['+l.ip+'] '+l.action+(l.detail?' — '+l.detail:'')+'</div>';
  }).join('');
}

async function loadFileLogs(){
  const box=document.getElementById('log-box');
  box.textContent='載入中...';
  const r=await adm('/admin/logfile');
  box.textContent=r.content||( r.error?'❌ '+r.error:'（空）');
  box.scrollTop=box.scrollHeight;
}

async function loadEnv(){
  const r=await adm('/admin/config');
  if(r.content!==undefined)document.getElementById('env-ta').value=r.content;
}

async function saveEnv(){
  const content=document.getElementById('env-ta').value;
  const r=await adm('/admin/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})});
  const m=document.getElementById('msg');
  if(r.ok){m.className='ok';m.textContent='✅ 已儲存，重啟後生效';}
  else{m.className='err';m.textContent='❌ '+(r.error||'');}
  setTimeout(()=>m.style.display='none',3000);
}

async function clrLog(){
  if(!confirm('清除所有訪問日誌？'))return;
  await adm('/admin/logs/clear');
  document.getElementById('log-box').textContent='已清除';
}
init();
</script></body></html>"""

@app.route("/admin")
def admin_page():
    if not admin_auth(request): return redirect("/admin/login")
    html = (ADMIN_HTML
        .replace("%%VER%%", __version__)
        .replace("%%PORT%%", str(PORT))
        .replace("%%KEY%%", SECRET_KEY)
        .replace("%%ADMIN%%", ADMIN_KEY)
        .replace("%%REPO%%", GH_REPO))
    resp = make_response(Response(html, mimetype="text/html"))
    resp.set_cookie("admin", ADMIN_KEY, max_age=24*3600)
    return resp

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        k = request.form.get("key","")
        if k == ADMIN_KEY:
            resp = make_response(redirect("/admin"))
            resp.set_cookie("admin", k, max_age=24*3600)
            return resp
        error = "管理員密鑰錯誤"
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin Login</title></head>
<body style="margin:0;font-family:-apple-system,sans-serif;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;min-height:100vh">
<div style="width:100%;max-width:320px;padding:40px 24px;text-align:center">
<div style="font-size:40px;margin-bottom:12px">⚙️</div>
<div style="font-size:22px;font-weight:700;margin-bottom:32px">管理員登入</div>
{"" if not error else f'<div style="background:rgba(255,59,48,.15);color:#ff453a;padding:10px;border-radius:10px;font-size:13px;margin-bottom:14px">{error}</div>'}
<form method="post" action="/admin/login">
<input name="key" type="password" placeholder="管理員密鑰" autofocus
  style="width:100%;background:#1c1c1e;border:none;color:#fff;padding:14px 16px;border-radius:12px;font-size:16px;margin-bottom:12px;font-family:inherit;outline:none">
<button type="submit"
  style="width:100%;background:#5856d6;color:#fff;border:none;padding:14px;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer">進入</button>
</form></div></body></html>"""


# ── Admin API ─────────────────────────────────────────────────────────────────

@app.route("/admin/check_update")
def check_update():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    import urllib.request as urlreq
    try:
        mirrors = [
            f"https://raw.githubusercontent.com/{GH_REPO}/main/version.txt",
            f"https://cdn.jsdelivr.net/gh/{GH_REPO}@main/version.txt",
        ]
        remote = None
        for url in mirrors:
            try:
                req = urlreq.Request(url, headers={"User-Agent":"SchoolSystem/1.0"})
                with urlreq.urlopen(req, timeout=10) as r:
                    remote = r.read().decode().strip()
                if remote: break
            except (OSError, ValueError):
                continue
        if not remote: return jsonify({"error":"Cannot reach GitHub"}),500
        return jsonify({"current":__version__,"remote_version":remote,"has_update":remote!=__version__})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/admin/update")
def do_update():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    import subprocess, urllib.request as urlreq
    base = os.path.dirname(os.path.abspath(__file__))
    method_used = ""
    errors = []

    # Method 1: git pull (fastest, most reliable)
    try:
        r = subprocess.run(
            ["git", "-C", base, "pull", "origin", "main"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0:
            method_used = "git pull"
            updated = [l.strip() for l in r.stdout.split("\n") if "|" in l or "changed" in l]
            if not updated: updated = ["(already up to date or pulled)"]
            def restart():
                time.sleep(2)
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".restart_requested"), "w") as f:
                    pass
                os.kill(os.getpid(), 15)
            threading.Thread(target=restart,daemon=True).start()
            return jsonify({"ok":True,"method":method_used,"updated":updated,"msg":"Git pull OK, restarting..."})
        else:
            errors.append(f"git pull failed: {r.stderr.strip()}")
    except Exception as e:
        errors.append(f"git error: {e}")

    # Method 2: HTTP download from multiple mirrors
    files = ["main.py","ui.py","timetable.py","recording.py","version.txt"]
    mirrors = [
        f"https://cdn.jsdelivr.net/gh/{GH_REPO}@main/",
        f"https://raw.githubusercontent.com/{GH_REPO}/main/",
        f"https://github.com/{GH_REPO}/raw/refs/heads/main/",
    ]
    updated = []
    for fname in files:
        content = None
        last_err = ""
        for mirror in mirrors:
            try:
                req = urlreq.Request(mirror+fname,
                    headers={"User-Agent":"SchoolSystem-Updater/1.0","Cache-Control":"no-cache"})
                with urlreq.urlopen(req, timeout=20) as r:
                    content = r.read()
                if content and len(content) > 10:
                    break
                content = None
            except Exception as e:
                last_err = str(e)
                continue
        if content:
            fpath = os.path.join(base, fname)
            if os.path.exists(fpath):
                shutil.copy(fpath, fpath+".bak")
            with open(fpath,"wb") as out:
                out.write(content)
            updated.append(fname)
        else:
            errors.append(f"{fname}: {last_err}")

    if not updated:
        return jsonify({
            "error": "All download methods failed",
            "details": errors,
            "hint": "Check if Redmi can access github.com / cdn.jsdelivr.net"
        }), 500

    method_used = "HTTP download"
    def restart():
        time.sleep(2)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".restart_requested"), "w") as f:
            pass
        os.kill(os.getpid(), 15)
    threading.Thread(target=restart,daemon=True).start()
    return jsonify({"ok":True,"method":method_used,"updated":updated,"errors":errors,"msg":"Restarting..."})

@app.route("/admin/rollback")
def rollback():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        for fname in ["main.py","ui.py"]:
            bak = os.path.join(base, fname+".bak")
            dst = os.path.join(base, fname)
            if os.path.exists(bak): shutil.copy(bak, dst)
        def restart():
            time.sleep(1)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".restart_requested"), "w") as f:
                pass
            os.kill(os.getpid(), 15)
        threading.Thread(target=restart, daemon=True).start()
        return jsonify({"ok":True})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/admin/restart")
def admin_restart():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    def do():
        time.sleep(1)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".restart_requested"), "w") as f:
            pass
        os.kill(os.getpid(), 15)
    threading.Thread(target=do, daemon=True).start()
    return jsonify({"ok":True})

@app.route("/admin/config", methods=["GET"])
def config_get():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    try:
        with open(ENV_PATH,"r") as f: content = f.read()
        return jsonify({"content":content})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/admin/config", methods=["POST"])
def config_post():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    d = request.get_json()
    if not d or "content" not in d: return jsonify({"error":"no content"}),400
    try:
        shutil.copy(ENV_PATH, ENV_PATH+".bak")
        with open(ENV_PATH,"w") as f: f.write(d["content"])
        return jsonify({"ok":True})
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route("/admin/dbsize")
def dbsize():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    db_size = os.path.getsize(DB_PATH) // 1024 if os.path.exists(DB_PATH) else 0
    rec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
    rec_size = 0
    if os.path.isdir(rec_dir):
        for f in os.listdir(rec_dir):
            fp = os.path.join(rec_dir, f)
            if os.path.isfile(fp):
                rec_size += os.path.getsize(fp)
        rec_size = rec_size // 1024
    return jsonify({"db_kb": db_size, "rec_kb": rec_size})

@app.route("/admin/logfile")
def admin_logfile():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
        content = "".join(lines[-200:])
        return jsonify({"content": content})
    except FileNotFoundError:
        return jsonify({"content": "（log.txt 不存在）"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/logs/clear")
def logs_clear():
    if not admin_auth(request): return jsonify({"error":"unauthorized"}),401
    db = get_db()
    db.execute("DELETE FROM access_log")
    db.commit()
    return jsonify({"ok":True})


# ── Whiteboard ────────────────────────────────────────────────────────────────

@app.route("/api/whiteboard/upload", methods=["POST"])
def whiteboard_upload():
    if not auth(request): return jsonify({"error":"unauthorized"}),401
    if "file" not in request.files:
        return jsonify({"error":"no file"}),400
    f = request.files["file"]
    import base64
    img_data = base64.b64encode(f.read()).decode()
    ext = "jpeg"
    if f.filename.lower().endswith(".png"): ext = "png"
    elif f.filename.lower().endswith(".heic"): ext = "heic"
    wb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "whiteboards")
    os.makedirs(wb_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fpath = os.path.join(wb_dir, f"{ts}.{ext}")
    with open(fpath, "wb") as out:
        out.write(base64.b64decode(img_data))
    result = {"ok":True,"filename":f"{ts}.{ext}","b64":img_data,"ext":ext}
    if DEEPSEEK_KEY:
        try:
            import urllib.request as urlreq, json as _json
            payload = _json.dumps({"model":"deepseek-chat","max_tokens":600,
                "messages":[{"role":"user","content":[
                    {"type":"text","text":'呢張係香港中學白板嘅功課記錄，請提取所有功課項目，每項包括：科目、功課描述、截止日期（如有）。用JSON格式回覆，格式：{"homeworks":[{"subject":"","title":"","due_date":""}]}。如果睇唔清就返回空list。'},
                    {"type":"image_url","image_url":{"url":f"data:image/{ext};base64,{img_data}"}}
                ]}]}).encode()
            req = urlreq.Request("https://api.deepseek.com/chat/completions",
                data=payload,
                headers={"Content-Type":"application/json","Authorization":f"Bearer {DEEPSEEK_KEY}"},
                method="POST")
            with urlreq.urlopen(req, timeout=30) as r:
                resp = _json.loads(r.read())
            text = resp["choices"][0]["message"]["content"]
            try:
                import re as _re
                m = _re.search(r'\{.*\}', text, _re.DOTALL)
                if m:
                    parsed = _json.loads(m.group())
                    result["homeworks"] = parsed.get("homeworks",[])
                    result["raw"] = text
            except (json.JSONDecodeError, ValueError):
                result["raw"] = text
        except Exception as e:
            result["ai_error"] = str(e)
    return jsonify(result)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print(f"[SchoolSystem] v{__version__} on {HOST}:{PORT}")
    if os.getenv("DISCORD_TOKEN",""):
        try:
            from bot import run_bot
            bot_thread = threading.Thread(target=run_bot, daemon=True)
            bot_thread.start()
            print("[Bot] Discord bot starting...")
        except Exception as e:
            print(f"[Bot] Failed to start: {e}")
    else:
        print("[Bot] No DISCORD_TOKEN, skipping")
    app.run(host=HOST, port=PORT, debug=False)
