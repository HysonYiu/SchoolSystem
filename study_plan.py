"""
Study Plan Generator
優先級：考試日期 + 空堂 + 假期 + 功課量
平日 18:00 後，假期全日
"""
import json
import os
import sqlite3
from datetime import date, datetime, timedelta

from dotenv import load_dotenv

from timetable import ALL_NO_SCHOOL, TIMETABLE, get_cycle_day, is_school_day

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schoolsystem.db")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# ── 空堂識別 ─────────────────────────────────────────────────────────────────
# 非主科時段可用於溫書
STUDY_SUBJECTS = {"MATH","M2","CHEM","ENG","CHI","ICT","LS","LIFE-ED"}
FREE_SLOTS = {"OLE","CSD","PE","LIFE-ED"}  # 較輕鬆，可用於溫書

def get_free_periods(day_num):
    """返回今日可用於溫書的空堂"""
    slots = TIMETABLE.get(day_num, [])
    free = []
    for s in slots:
        if s[2] in FREE_SLOTS:
            free.append({"start": s[0], "end": s[1], "type": s[2], "room": s[3]})
    return free

def get_study_context(days_ahead=7):
    """收集溫書計劃所需的完整上下文"""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    # 未完成功課
    hw = db.execute(
        "SELECT * FROM homeworks WHERE done=0 ORDER BY due_date ASC, priority ASC LIMIT 30"
    ).fetchall()

    # 即將考試
    exams = db.execute(
        "SELECT *, julianday(exam_date)-julianday('now') as days_left "
        "FROM exams WHERE exam_date>=date('now') ORDER BY exam_date ASC"
    ).fetchall()
    db.close()

    # 未來 7 日的時間分析
    schedule = []
    today = date.today()
    for i in range(days_ahead):
        d = today + timedelta(days=i)
        ds = d.isoformat()
        school = is_school_day(d)
        day_num = get_cycle_day(d) if school else None

        free_periods = get_free_periods(day_num) if day_num else []

        # 計算可用溫書時間
        if not school:
            available_hours = 8.0  # 假期全日
            day_type = "假期/週末"
        else:
            available_hours = 3.5  # 平日 18:00-21:30
            day_type = f"上學日 Day{day_num}"

        # 檢查當日截止功課
        due_today = [dict(h) for h in hw if h["due_date"] == ds]
        due_tmr = [dict(h) for h in hw if h["due_date"] == (d + timedelta(days=1)).isoformat()]

        schedule.append({
            "date": ds,
            "weekday": ["一","二","三","四","五","六","日"][d.weekday()],
            "type": day_type,
            "day_num": day_num,
            "available_hours": available_hours,
            "free_periods": free_periods,
            "hw_due": due_today,
            "hw_due_tomorrow": due_tmr,
        })

    return {
        "today": today.isoformat(),
        "homeworks": [dict(h) for h in hw],
        "exams": [dict(e) for e in exams],
        "schedule": schedule,
    }

def generate_study_plan(focus_days=3):
    """用 DeepSeek 生成溫書計劃"""
    if not DEEPSEEK_KEY:
        return {"error": "no_key"}

    ctx = get_study_context(days_ahead=focus_days)

    # 建立結構化 prompt
    hw_list = "\n".join([
        f"- [{h['priority']}優先][{h['subject']}] {h['title']} "
        f"截止:{h.get('due_date','未知')} 類型:{h['hw_type']}"
        for h in ctx["homeworks"][:15]
    ]) or "（暫無待做功課）"

    exam_list = "\n".join([
        f"- [{e['subject']}] {e.get('title','')} "
        f"日期:{e['exam_date']} 剩{int(e.get('days_left',0))}天 "
        f"範圍:{e.get('scope','未知')}"
        for e in ctx["exams"]
    ]) or "（暫無即將考試）"

    schedule_list = "\n".join([
        f"- {s['date']}(星期{s['weekday']}) [{s['type']}] "
        f"可用:{s['available_hours']}小時"
        + (f" 空堂:{','.join([p['type'] for p in s['free_periods']])}" if s['free_periods'] else "")
        + (f" ⚠️當日截止:{len(s['hw_due'])}項" if s['hw_due'] else "")
        for s in ctx["schedule"]
    ])

    prompt = f"""你係香港DSE中四學生嘅學習助手。請根據以下資料生成詳細溫書計劃。

【未完成功課】
{hw_list}

【即將考試/小測】
{exam_list}

【未來{focus_days}日時間表】
{schedule_list}

【規則】
- 平日放學後18:00先開始溫書
- 假期/週末可全日溫書
- 空堂（OLE/CSD/PE課）可用嚟做功課
- 高優先級功課先做
- 考試前要集中溫習相關科目
- MATH/M2功課可能係同一老師出，要一齊計劃

請輸出：
1. 今日/明日重點待做事項（清單格式）
2. 未來{focus_days}日每日詳細時間分配
3. 考試前溫習建議

用廣東話，格式清晰易讀，重點突出。"""

    try:
        import urllib.request as urlreq
        payload = json.dumps({
            "model": "deepseek-reasoner",
            "max_tokens": 1200,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        req = urlreq.Request(
            "https://api.deepseek.com/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {DEEPSEEK_KEY}"},
            method="POST"
        )
        with urlreq.urlopen(req, timeout=45) as r:
            result = json.loads(r.read())
        return {
            "ok": True,
            "plan": result["choices"][0]["message"]["content"],
            "context": ctx
        }
    except Exception as e:
        return {"error": str(e)}

def get_today_priorities():
    """快速獲取今日優先事項（不用 AI）"""
    ctx = get_study_context(days_ahead=1)
    today = ctx["schedule"][0] if ctx["schedule"] else {}
    today_str = date.today().isoformat()
    tmr_str = (date.today() + timedelta(days=1)).isoformat()

    hw = ctx["homeworks"]
    urgent = [h for h in hw if h.get("due_date","") <= today_str and h.get("due_date","")]
    tomorrow = [h for h in hw if h.get("due_date","") == tmr_str]
    high_pri = [h for h in hw if h.get("priority") == "高" and h not in urgent]

    return {
        "urgent": urgent,
        "due_tomorrow": tomorrow,
        "high_priority": high_pri,
        "free_periods": today.get("free_periods", []),
        "available_hours": today.get("available_hours", 3.5),
        "day_type": today.get("type", ""),
        "exams_soon": [e for e in ctx["exams"] if int(e.get("days_left", 99)) <= 7]
    }
