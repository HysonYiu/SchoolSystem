import os
import sqlite3
from datetime import datetime

from flask import Blueprint, jsonify, request, send_file

recording_bp = Blueprint("recording", __name__)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
REC_DIR    = os.path.join(BASE_DIR, "recordings")
DB_PATH    = os.path.join(BASE_DIR, "schoolsystem.db")

os.makedirs(REC_DIR, exist_ok=True)


def _secret():
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv("SECRET_KEY", "changeme")

def _auth(req):
    k = req.args.get("key") or req.headers.get("X-API-Key") or req.cookies.get("key")
    return k == _secret()

def _db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS recordings (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        filename    TEXT NOT NULL,
        subject     TEXT DEFAULT '',
        cycle_day   INTEGER,
        period      TEXT DEFAULT '',
        rec_date    TEXT DEFAULT (date('now','localtime')),
        file_size   INTEGER DEFAULT 0,
        notes       TEXT DEFAULT '',
        created_at  TEXT DEFAULT (datetime('now','localtime'))
    )""")
    db.commit()
    return db


@recording_bp.route("/api/recordings", methods=["GET"])
def rec_list():
    if not _auth(request): return jsonify({"error":"unauthorized"}), 401
    db = _db()
    subj = request.args.get("subject","")
    q = "SELECT * FROM recordings"
    p = []
    if subj:
        q += " WHERE subject=?"; p.append(subj)
    q += " ORDER BY created_at DESC LIMIT 100"
    rows = db.execute(q, p).fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@recording_bp.route("/api/recordings/upload", methods=["POST"])
def rec_upload():
    if not _auth(request): return jsonify({"error":"unauthorized"}), 401
    if "file" not in request.files:
        return jsonify({"error":"no file"}), 400
    f       = request.files["file"]
    subject = request.form.get("subject","")
    period  = request.form.get("period","")
    notes   = request.form.get("notes","")
    cycle   = request.form.get("cycle_day","")
    ext     = ".webm"
    fn      = f.filename.lower()
    for e in [".mp4",".m4a",".ogg",".wav",".aac",".mp3"]:
        if fn.endswith(e): ext = e; break
    ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{ts}_{subject}{ext}"
    fpath = os.path.join(REC_DIR, fname)
    f.save(fpath)
    size  = os.path.getsize(fpath)
    db    = _db()
    db.execute("INSERT INTO recordings(filename,subject,cycle_day,period,file_size,notes) VALUES(?,?,?,?,?,?)",
               (fname, subject, cycle or None, period, size, notes))
    db.commit()
    new_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    return jsonify({"ok":True,"id":new_id,"filename":fname})


@recording_bp.route("/api/recordings/<int:rec_id>", methods=["GET"])
def rec_serve(rec_id):
    if not _auth(request): return jsonify({"error":"unauthorized"}), 401
    db  = _db()
    row = db.execute("SELECT * FROM recordings WHERE id=?",(rec_id,)).fetchone()
    db.close()
    if not row: return jsonify({"error":"not found"}), 404
    fpath = os.path.join(REC_DIR, row["filename"])
    if not os.path.exists(fpath): return jsonify({"error":"file missing"}), 404
    mime = "audio/mpeg" if row["filename"].endswith(".mp3") else "audio/mp4" if row["filename"].endswith((".mp4",".m4a")) else "audio/webm"
    return send_file(fpath, mimetype=mime)


@recording_bp.route("/api/recordings/<int:rec_id>", methods=["DELETE"])
def rec_delete(rec_id):
    if not _auth(request): return jsonify({"error":"unauthorized"}), 401
    db  = _db()
    row = db.execute("SELECT filename FROM recordings WHERE id=?",(rec_id,)).fetchone()
    if row:
        fpath = os.path.join(REC_DIR, row["filename"])
        if os.path.exists(fpath): os.remove(fpath)
        db.execute("DELETE FROM recordings WHERE id=?", (rec_id,))
        db.commit()
    db.close()
    return jsonify({"ok":True})


@recording_bp.route("/api/recordings/<int:rec_id>/notes", methods=["POST"])
def rec_notes(rec_id):
    if not _auth(request): return jsonify({"error":"unauthorized"}), 401
    d = request.get_json()
    if not d: return jsonify({"error":"no data"}), 400
    db = _db()
    db.execute("UPDATE recordings SET notes=? WHERE id=?",(d.get("notes",""),rec_id))
    db.commit()
    db.close()
    return jsonify({"ok":True})
