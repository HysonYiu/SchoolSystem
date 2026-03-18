"""
agent.py — SchoolSystem AI Agent Engine
OrchestratorAgent + SubAgents with full system context
"""
import os, sqlite3, json
from datetime import datetime, date, timedelta

DB_PATH     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schoolsystem.db")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

SUBJECTS = ["CHI","ENG","MATH","M2","CHEM","ICT","LS","LIFE-ED","CSD","PE","OLE"]
HW_TYPES = ["功課","小測","考試","報告","Project","默書","實驗","課堂練習"]

# ── System context ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """你係 SchoolSystem 嘅智能學習助手，為香港 DSE 學生服務。

## 你的身份
- 你係一個全能學習管家，有完整嘅學校資料存取權限
- 學校：[User's School]
- 制度：DSE，7日 Cycle 循環課表

## 你的科目
必修：中文(CHI)、英文(ENG)、數學(MATH)、通識/公社(LS)
選修：M2（數學延伸）、化學(CHEM)、資訊科技(ICT)

## 重要科目備注
- MATH 同 M2 係同一個老師(老師36)，任何時段都可能上 M2 或 MATH
- CHEM 老師每日更新 PDF，包含功課、溫書資料
- ICT 老師主要用 Google Classroom 同 WhatsApp 佈置功課
- LIFE-ED 同 ENG 係隔週交替（同一時段）

## 你的權限
你可以：
✅ 查看所有功課、考試、錄音記錄
✅ 分析學習狀況、優先排序
✅ 生成詳細溫書計劃
✅ 建議加入功課（會明確列出建議，用戶確認後執行）
✅ 標記功課優先級
✅ 提供各科學習策略

## 溫書計劃規則
- 平日：18:00 後先開始溫書
- 假期/非上學日：全日可用
- 考試優先順序：截止最近 > 優先級高 > 功課量多嘅科目
- 每科溫書時間建議：30-90分鐘為佳，唔好超過2小時

## 回答風格
- 用廣東話回答（可以中英夾雜）
- 簡潔清晰，用列表格式
- 如有功課建議，列明：科目、內容、建議時間
- 考試臨近時主動提醒

## 重要提示
- 你係私人助手，只服務 SchoolSystem 一人
- 所有數據都係真實學校資料，認真對待
- 如果唔確定，主動問清楚先建議
"""

# ── DB helpers ────────────────────────────────────────────────────────────────

def _db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def get_full_context(cycle_day=None):
    """Build complete context for AI — homework, exams, timetable, stats."""
    db = _db()
    today = date.today().isoformat()

    # All pending homework
    hw_all = db.execute(
        "SELECT * FROM homeworks WHERE done=0 ORDER BY due_date ASC, priority ASC"
    ).fetchall()

    # Overdue
    hw_overdue = [h for h in hw_all if h["due_date"] and h["due_date"] < today]

    # Due today
    hw_today = [h for h in hw_all if h["due_date"] == today]

    # Due this week
    week_end = (date.today() + timedelta(days=7)).isoformat()
    hw_week = [h for h in hw_all if h["due_date"] and today <= h["due_date"] <= week_end]

    # Exams
    exams = db.execute(
        "SELECT *, julianday(exam_date)-julianday('now') as days_left FROM exams ORDER BY exam_date ASC"
    ).fetchall()

    # Stats
    total  = db.execute("SELECT COUNT(*) FROM homeworks").fetchone()[0]
    done   = db.execute("SELECT COUNT(*) FROM homeworks WHERE done=1").fetchone()[0]
    by_subj = db.execute(
        "SELECT subject, COUNT(*) as cnt FROM homeworks WHERE done=0 GROUP BY subject ORDER BY cnt DESC"
    ).fetchall()

    # Recent recordings
    recordings = db.execute(
        "SELECT subject, period, rec_date FROM recordings ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    db.close()

    ctx = {
        "today": today,
        "cycle_day": cycle_day,
        "stats": {
            "total": total,
            "done": done,
            "pending": total - done,
            "completion_rate": f"{round(done / total * 100)}%" if total else "0%"
        },
        "homework": {
            "overdue": [_hw_dict(h) for h in hw_overdue],
            "due_today": [_hw_dict(h) for h in hw_today],
            "due_this_week": [_hw_dict(h) for h in hw_week],
            "all_pending": [_hw_dict(h) for h in hw_all[:30]]
        },
        "exams": [_exam_dict(e) for e in exams],
        "by_subject": [dict(r) for r in by_subj],
        "recent_recordings": [dict(r) for r in recordings]
    }
    return ctx

def _hw_dict(h):
    return {
        "id": h["id"],
        "title": h["title"],
        "subject": h["subject"],
        "type": h["hw_type"],
        "due": h["due_date"],
        "priority": h["priority"],
        "notes": h["notes"]
    }

def _exam_dict(e):
    return {
        "id": e["id"],
        "subject": e["subject"],
        "title": e["title"],
        "date": e["exam_date"],
        "days_left": round(e["days_left"]) if e["days_left"] is not None else None,
        "scope": e["scope"]
    }


# ── AI call ───────────────────────────────────────────────────────────────────

def call_deepseek(messages, max_tokens=1200, use_reasoner=True):
    """Call DeepSeek API with full error handling."""
    import urllib.request as urlreq

    if not DEEPSEEK_KEY:
        return None, "no_key"

    model = "deepseek-reasoner" if use_reasoner else "deepseek-chat"

    payload = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages
    }).encode()

    req = urlreq.Request(
        DEEPSEEK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}"
        },
        method="POST"
    )

    try:
        with urlreq.urlopen(req, timeout=45) as r:
            result = json.loads(r.read())
        answer = result["choices"][0]["message"]["content"]
        return answer, None
    except Exception as e:
        return None, str(e)


# ── OrchestratorAgent ─────────────────────────────────────────────────────────

def orchestrate(question, cycle_day=None, action_hint=None):
    """
    Main entry point. Routes to appropriate handler based on question.
    Returns: {"answer": str, "action": dict|None, "error": str|None}
    """
    ctx = get_full_context(cycle_day)

    # Determine task type
    q_lower = question.lower()

    if any(k in q_lower for k in ["溫書計劃","study plan","today plan","今晚","今日計劃"]):
        return study_plan_agent(ctx)

    if any(k in q_lower for k in ["最緊急","urgent","截止","due","overdue","逾期"]):
        return priority_agent(ctx)

    if any(k in q_lower for k in ["考試","exam","test","小測","默書"]):
        return exam_agent(ctx)

    if any(k in q_lower for k in ["統計","progress","完成","completion","done"]):
        return stats_agent(ctx)

    if any(k in q_lower for k in ["加功課","add homework","記錄","幫我加"]):
        return add_hw_agent(question, ctx)

    # General Q&A
    return general_agent(question, ctx)


# ── SubAgents ─────────────────────────────────────────────────────────────────

def study_plan_agent(ctx):
    """Generate detailed study plan for tonight."""
    today = ctx["today"]
    cd = ctx["cycle_day"]
    pending = ctx["homework"]["all_pending"]
    overdue = ctx["homework"]["overdue"]
    exams = ctx["exams"]

    prompt = f"""今日：{today}，Cycle Day {cd}

**逾期功課（最優先）：**
{json.dumps(overdue, ensure_ascii=False, indent=2) if overdue else "無"}

**今日截止：**
{json.dumps(ctx["homework"]["due_today"], ensure_ascii=False, indent=2) if ctx["homework"]["due_today"] else "無"}

**本週截止功課：**
{json.dumps(ctx["homework"]["due_this_week"][:10], ensure_ascii=False, indent=2)}

**即將考試：**
{json.dumps([e for e in exams if e["days_left"] is not None and e["days_left"] <= 14], ensure_ascii=False, indent=2) if exams else "無"}

**各科功課量：**
{json.dumps(ctx["by_subject"], ensure_ascii=False)}

請根據以上資料，為 SchoolSystem 生成今晚嘅詳細溫書計劃：
1. 18:00-22:00 時間分配（每個時段30-90分鐘）
2. 按緊急程度排序
3. 每科具體要做咩
4. 估計完成時間
5. 注意事項

用廣東話，清晰列表格式。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    answer, err = call_deepseek(messages, max_tokens=1500)
    if err:
        return {"answer": None, "error": err}
    return {"answer": answer, "action": None, "agent": "StudyPlanAgent"}


def priority_agent(ctx):
    """Analyze and rank homework by urgency."""
    all_hw = ctx["homework"]["all_pending"]
    exams = ctx["exams"]

    prompt = f"""今日：{ctx["today"]}，Cycle Day {ctx["cycle_day"]}

**所有待做功課：**
{json.dumps(all_hw[:20], ensure_ascii=False, indent=2)}

**考試：**
{json.dumps(exams[:5], ensure_ascii=False, indent=2) if exams else "無"}

請分析並列出：
1. 🔴 最緊急（今日/明日截止或逾期）
2. 🟡 本週內需完成
3. 🟢 可以遲少少做

每項說明原因，並估計需要多少時間完成。用廣東話。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    answer, err = call_deepseek(messages, max_tokens=1000)
    if err:
        return {"answer": None, "error": err}
    return {"answer": answer, "action": None, "agent": "PriorityAgent"}


def exam_agent(ctx):
    """Provide exam preparation strategy."""
    exams = ctx["exams"]
    all_hw = ctx["homework"]["all_pending"]

    upcoming = [e for e in exams if e["days_left"] is not None and e["days_left"] >= 0]

    prompt = f"""今日：{ctx["today"]}，Cycle Day {ctx["cycle_day"]}

**即將考試：**
{json.dumps(upcoming, ensure_ascii=False, indent=2) if upcoming else "暫無考試記錄"}

**相關科目待做功課：**
{json.dumps([h for h in all_hw if any(e["subject"] == h["subject"] for e in upcoming)][:10], ensure_ascii=False, indent=2)}

請提供：
1. 每個考試嘅倒數同緊急程度
2. 針對每科嘅溫書策略
3. 建議溫書順序
4. DSE 應試貼士（如適用）

用廣東話，實用具體。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    answer, err = call_deepseek(messages, max_tokens=1000)
    if err:
        return {"answer": None, "error": err}
    return {"answer": answer, "action": None, "agent": "ExamAgent"}


def stats_agent(ctx):
    """Analyze learning progress and provide feedback."""
    stats = ctx["stats"]
    by_subj = ctx["by_subject"]

    prompt = f"""今日：{ctx["today"]}

**學習統計：**
- 總功課數：{stats["total"]}
- 已完成：{stats["done"]}
- 待做：{stats["pending"]}
- 完成率：{stats["completion_rate"]}

**各科待做功課量：**
{json.dumps(by_subj, ensure_ascii=False, indent=2)}

**逾期功課：**
{len(ctx["homework"]["overdue"])} 項

請提供：
1. 整體學習狀況評估
2. 哪科需要特別關注
3. 改善建議
4. 鼓勵性總結

用廣東話，客觀分析。"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    answer, err = call_deepseek(messages, max_tokens=800, use_reasoner=False)
    if err:
        return {"answer": None, "error": err}
    return {"answer": answer, "action": None, "agent": "StatsAgent"}


def add_hw_agent(question, ctx):
    """Extract homework details from natural language and suggest adding."""
    prompt = f"""用戶說：「{question}」

請從呢句話提取功課資料，如果資料不完整請指出。
回覆 JSON 格式：
{{
  "understood": true/false,
  "title": "功課標題",
  "subject": "科目（必須係：{', '.join(SUBJECTS)} 其中之一）",
  "hw_type": "類型（必須係：{', '.join(HW_TYPES)} 其中之一）",
  "due_date": "YYYY-MM-DD 或 null",
  "priority": "高/中/低",
  "notes": "備註",
  "missing": ["缺少咩資料"]
}}

只回覆 JSON，唔好其他文字。"""

    messages = [
        {"role": "system", "content": "你係資料提取助手，只回覆 JSON。"},
        {"role": "user", "content": prompt}
    ]

    answer, err = call_deepseek(messages, max_tokens=300, use_reasoner=False)
    if err:
        return {"answer": None, "error": err}

    try:
        # Clean JSON response
        clean = answer.strip().strip("```json").strip("```").strip()
        data = json.loads(clean)

        if data.get("understood") and not data.get("missing"):
            return {
                "answer": f"我理解你想加：\n📚 **{data['title']}**\n科目：{data['subject']} | 類型：{data['hw_type']} | 截止：{data.get('due_date','未指定')} | 優先：{data['priority']}\n\n確認加入功課表？",
                "action": {"type": "add_hw", "data": data},
                "agent": "AddHWAgent"
            }
        else:
            missing = "、".join(data.get("missing", []))
            return {
                "answer": f"我明白你想加功課，但需要多啲資料：{missing}\n請補充後重新告訴我。",
                "action": None,
                "agent": "AddHWAgent"
            }
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return {
            "answer": "唔好意思，請直接用「加功課」頁面加入，或者詳細描述功課（科目、標題、截止日期）。",
            "action": None,
            "agent": "AddHWAgent"
        }


def general_agent(question, ctx):
    """Handle general questions with full context."""
    ctx_summary = f"""今日：{ctx["today"]}，Cycle Day {ctx["cycle_day"]}
待做功課：{ctx["stats"]["pending"]} 項（逾期：{len(ctx["homework"]["overdue"])} 項）
即將考試：{len(ctx["exams"])} 個
完成率：{ctx["stats"]["completion_rate"]}

功課詳情：{json.dumps(ctx["homework"]["all_pending"][:15], ensure_ascii=False)}
考試：{json.dumps(ctx["exams"][:5], ensure_ascii=False)}"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\n## 當前數據\n" + ctx_summary},
        {"role": "user", "content": question}
    ]

    answer, err = call_deepseek(messages, max_tokens=1000)
    if err:
        return {"answer": None, "error": err}
    return {"answer": answer, "action": None, "agent": "GeneralAgent"}
