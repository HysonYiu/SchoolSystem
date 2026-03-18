import os, asyncio, sqlite3, threading
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN       = os.getenv("DISCORD_TOKEN","")
GUILD_ID    = int(os.getenv("DISCORD_GUILD_ID","0"))
CH_HOMEWORK = int(os.getenv("DISCORD_CH_HOMEWORK","0"))
CH_AI       = int(os.getenv("DISCORD_CH_AI","0"))
CH_SYSTEM   = int(os.getenv("DISCORD_CH_SYSTEM","0"))
CH_EXAM     = int(os.getenv("DISCORD_CH_EXAM","0"))
USER_ID     = int(os.getenv("DISCORD_USER_ID","0"))
DB_PATH     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schoolsystem.db")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")
REMIND_TIME = os.getenv("DAILY_REMINDER_TIME","07:30")

import discord
from discord import app_commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree   = app_commands.CommandTree(client)


# ── DB helpers ────────────────────────────────────────────────────────────────

def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def get_hw(done=0, subject=None, limit=20):
    c = db()
    q = "SELECT * FROM homeworks WHERE done=?"
    p = [done]
    if subject:
        q += " AND subject=?"; p.append(subject)
    q += " ORDER BY due_date ASC LIMIT ?"
    p.append(limit)
    rows = c.execute(q, p).fetchall()
    c.close()
    return [dict(r) for r in rows]

def get_exams(upcoming_only=True):
    c = db()
    if upcoming_only:
        rows = c.execute(
            "SELECT *, julianday(exam_date)-julianday('now') as days_left "
            "FROM exams WHERE exam_date>=date('now') ORDER BY exam_date ASC"
        ).fetchall()
    else:
        rows = c.execute("SELECT * FROM exams ORDER BY exam_date DESC").fetchall()
    c.close()
    return [dict(r) for r in rows]

def add_hw(title, subject, hw_type="功課", due_date="", priority="中", notes=""):
    c = db()
    c.execute(
        "INSERT INTO homeworks(title,subject,hw_type,due_date,priority,notes,source) VALUES(?,?,?,?,?,?,?)",
        (title, subject, hw_type, due_date, priority, notes, "Discord")
    )
    c.commit(); c.close()

def mark_done(hw_id):
    c = db()
    c.execute("UPDATE homeworks SET done=1 WHERE id=?", (hw_id,))
    c.commit(); c.close()

def get_stats():
    c = db()
    total   = c.execute("SELECT COUNT(*) FROM homeworks").fetchone()[0]
    done    = c.execute("SELECT COUNT(*) FROM homeworks WHERE done=1").fetchone()[0]
    overdue = c.execute("SELECT COUNT(*) FROM homeworks WHERE done=0 AND due_date!='' AND due_date<date('now')").fetchone()[0]
    c.close()
    return {"total":total,"done":done,"pending":total-done,"overdue":overdue}


# ── Embeds ────────────────────────────────────────────────────────────────────

SUBJECT_COLORS = {
    "CHEM":0x0a84ff,"MATH":0x5856d6,"M2":0x5856d6,
    "ENG":0x34c759,"ICT":0xff9f0a,"CHI":0xff3b30,
    "LS":0x30d158,"LIFE-ED":0x30d158,
}

def hw_embed(hw_list, title="📝 功課列表"):
    if not hw_list:
        e = discord.Embed(title=title, description="🎉 暫無待做功課！", color=0x34c759)
        return e
    e = discord.Embed(title=title, color=0x5856d6)
    for h in hw_list[:10]:
        due = h.get("due_date","")
        if due:
            try:
                diff = (date.fromisoformat(due) - date.today()).days
                if diff < 0: due_str = f"⚠️ 逾期{abs(diff)}天"
                elif diff == 0: due_str = "🔴 今日截止"
                elif diff <= 2: due_str = f"🟡 {diff}天後"
                else: due_str = f"📅 {due}"
            except: due_str = due
        else:
            due_str = "無截止日期"
        pri = {"高":"🔴","中":"🟡","低":"🟢"}.get(h.get("priority","中"),"🟡")
        e.add_field(
            name=f"{pri} [{h['subject']}] {h['title']}",
            value=f"類型: {h.get('hw_type','功課')} | 截止: {due_str}",
            inline=False
        )
    if len(hw_list) > 10:
        e.set_footer(text=f"顯示前10項，共{len(hw_list)}項")
    return e

def exam_embed(exams):
    if not exams:
        e = discord.Embed(title="📅 考試列表", description="暫無即將考試", color=0x34c759)
        return e
    e = discord.Embed(title="📅 即將考試 & 小測", color=0xff9f0a)
    for ex in exams[:8]:
        dl = ex.get("days_left", 0)
        if dl is None: dl = 0
        dl = int(dl)
        if dl < 0: cd = "已過"
        elif dl == 0: cd = "🔴 今日！"
        elif dl <= 3: cd = f"🔴 {dl}天後"
        elif dl <= 7: cd = f"🟡 {dl}天後"
        else: cd = f"✅ {dl}天後 ({ex['exam_date']})"
        e.add_field(
            name=f"[{ex['subject']}] {ex.get('title',ex['subject']+' 考試')}",
            value=f"倒數: {cd}" + (f" | 範圍: {ex['scope']}" if ex.get('scope') else ""),
            inline=False
        )
    return e

def stats_embed():
    s = get_stats()
    rate = round(s["done"]/s["total"]*100) if s["total"] else 0
    e = discord.Embed(title="📊 學習統計", color=0x5856d6)
    e.add_field(name="總功課", value=str(s["total"]), inline=True)
    e.add_field(name="✅ 已完成", value=str(s["done"]), inline=True)
    e.add_field(name="⏳ 待做", value=str(s["pending"]), inline=True)
    e.add_field(name="⚠️ 逾期", value=str(s["overdue"]), inline=True)
    e.add_field(name="完成率", value=f"{rate}%", inline=True)
    e.set_footer(text=f"更新於 {datetime.now().strftime('%H:%M')}")
    return e


# ── AI helper ─────────────────────────────────────────────────────────────────

def ask_ai(question, context=""):
    if not DEEPSEEK_KEY:
        return "⚠️ 未設定 DEEPSEEK_API_KEY，請在管理員介面設定。"
    import urllib.request as urlreq, json
    hw  = get_hw(done=0, limit=15)
    exs = get_exams()
    ctx = f"今日{date.today()}。未完成功課：{hw}。即將考試：{exs}。{context}"
    payload = json.dumps({
        "model": "deepseek-reasoner",
        "max_tokens": 600,
        "messages": [
            {"role":"system","content":"你係香港中學生學習助手，熟悉DSE。用廣東話回答，簡潔清晰。背景："+ctx},
            {"role":"user","content": question}
        ]
    }).encode()
    try:
        req = urlreq.Request("https://api.deepseek.com/chat/completions",
            data=payload,
            headers={"Content-Type":"application/json","Authorization":f"Bearer {DEEPSEEK_KEY}"},
            method="POST")
        with urlreq.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ AI 錯誤：{e}"


# ── Slash Commands ────────────────────────────────────────────────────────────

@tree.command(name="hw", description="查看今日功課")
async def slash_hw(interaction: discord.Interaction):
    await interaction.response.defer()
    hw = get_hw(done=0)
    today_str = date.today().isoformat()
    today_hw = [h for h in hw if h.get("due_date","") <= today_str and h.get("due_date","")]
    all_hw   = [h for h in hw if not h.get("due_date","") or h.get("due_date","") > today_str]
    e = hw_embed(today_hw + all_hw, "📝 待做功課")
    await interaction.followup.send(embed=e)

@tree.command(name="today", description="今日待做功課")
async def slash_today(interaction: discord.Interaction):
    await interaction.response.defer()
    today_str = date.today().isoformat()
    hw = get_hw(done=0)
    today_hw = [h for h in hw if h.get("due_date","") and h.get("due_date","") <= today_str]
    e = hw_embed(today_hw, f"📅 今日待做 ({today_str})")
    await interaction.followup.send(embed=e)

@tree.command(name="add", description="加入功課")
@app_commands.describe(
    title="功課標題",
    subject="科目 (CHEM/MATH/M2/ENG/CHI/ICT/LS)",
    due="截止日期 (YYYY-MM-DD)",
    type="類型",
    priority="優先級 (高/中/低)"
)
async def slash_add(interaction: discord.Interaction,
                    title: str,
                    subject: str,
                    due: str = "",
                    type: str = "功課",
                    priority: str = "中"):
    try:
        add_hw(title, subject.upper(), type, due, priority)
        e = discord.Embed(
            title="✅ 功課已加入",
            description=f"**{title}**",
            color=0x34c759
        )
        e.add_field(name="科目", value=subject.upper(), inline=True)
        e.add_field(name="類型", value=type, inline=True)
        e.add_field(name="截止", value=due or "無", inline=True)
        e.add_field(name="優先", value=priority, inline=True)
        await interaction.response.send_message(embed=e)
    except Exception as ex:
        await interaction.response.send_message(f"❌ 錯誤：{ex}", ephemeral=True)

@tree.command(name="done", description="標記功課完成 (輸入功課ID)")
@app_commands.describe(hw_id="功課 ID (從 /hw 查看)")
async def slash_done(interaction: discord.Interaction, hw_id: int):
    try:
        mark_done(hw_id)
        await interaction.response.send_message(f"✅ 功課 #{hw_id} 已標記完成！", ephemeral=True)
    except Exception as ex:
        await interaction.response.send_message(f"❌ 錯誤：{ex}", ephemeral=True)

@tree.command(name="exam", description="查看即將考試")
async def slash_exam(interaction: discord.Interaction):
    await interaction.response.defer()
    exams = get_exams()
    e = exam_embed(exams)
    await interaction.followup.send(embed=e)

@tree.command(name="stats", description="查看學習統計")
async def slash_stats(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=stats_embed())

@tree.command(name="ask", description="問 AI 助手")
@app_commands.describe(question="你的問題")
async def slash_ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    answer = await asyncio.get_event_loop().run_in_executor(None, ask_ai, question)
    e = discord.Embed(
        title="🤖 AI 回覆",
        description=answer[:4000],
        color=0x5856d6
    )
    e.set_footer(text=f"問：{question[:50]}")
    await interaction.followup.send(embed=e)

@tree.command(name="study", description="AI 生成溫書計劃")
@app_commands.describe(days="計劃天數 (1/3/7, 預設3)")
async def slash_study(interaction: discord.Interaction, days: int = 3):
    await interaction.response.defer()
    try:
        from study_plan import generate_study_plan, get_today_priorities
        # First show priorities (fast, no AI)
        pri = get_today_priorities()
        urgent_count = len(pri.get("urgent",[]))
        tmr_count = len(pri.get("due_tomorrow",[]))
        exam_count = len(pri.get("exams_soon",[]))
        e = discord.Embed(title="⏳ 生成溫書計劃中...", color=0x5856d6)
        if urgent_count: e.add_field(name="🔴 今日截止", value=f"{urgent_count}項", inline=True)
        if tmr_count: e.add_field(name="🟡 明日截止", value=f"{tmr_count}項", inline=True)
        if exam_count: e.add_field(name="📅 7日內考試", value=f"{exam_count}個", inline=True)
        if pri.get("free_periods"):
            e.add_field(name="🕐 今日空堂", value="、".join([p["type"] for p in pri["free_periods"]]), inline=False)
        await interaction.followup.send(embed=e)
        # Generate AI plan
        result = await asyncio.get_event_loop().run_in_executor(None, generate_study_plan, days)
        if result.get("error") == "no_key":
            await interaction.followup.send("⚠️ 未設定 DEEPSEEK_API_KEY")
            return
        if result.get("error"):
            await interaction.followup.send(f"❌ {result['error']}")
            return
        plan_text = result["plan"]
        # Split if too long
        if len(plan_text) > 3900:
            plan_text = plan_text[:3900] + "..."
        plan_embed = discord.Embed(
            title=f"📅 {days}日溫書計劃",
            description=plan_text,
            color=0x0a84ff
        )
        plan_embed.set_footer(text=f"基於{len(result.get('context',{}).get('homeworks',[]))}項功課及考試時間表")
        await interaction.followup.send(embed=plan_embed)
    except Exception as ex:
        await interaction.followup.send(f"❌ 錯誤：{ex}", ephemeral=True)

@tree.command(name="cycle", description="查看今日係第幾 Day")
async def slash_cycle(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        from timetable import get_cycle_day, is_school_day
        today_date = date.today()
        day_num = get_cycle_day(today_date)
        school  = is_school_day(today_date)
        if school and day_num:
            e = discord.Embed(
                title=f"📋 今日係 Day {day_num}",
                description=f"日期：{today_date}",
                color=0x5856d6
            )
            from timetable import TIMETABLE
            slots = TIMETABLE.get(day_num, [])
            if slots:
                tt = "\n".join([f"`{s[0]}-{s[1]}` {s[2]} ({s[3]})" for s in slots])
                e.add_field(name="課程表", value=tt, inline=False)
        else:
            e = discord.Embed(title="🏠 今日非上學日", color=0x636366)
        await interaction.followup.send(embed=e)
    except Exception as ex:
        await interaction.followup.send(f"❌ {ex}", ephemeral=True)


# ── Scheduled Tasks ───────────────────────────────────────────────────────────

@tasks.loop(minutes=1)
async def daily_reminder():
    now = datetime.now().strftime("%H:%M")
    if now != REMIND_TIME:
        return
    ch_hw   = client.get_channel(CH_HOMEWORK)
    ch_exam = client.get_channel(CH_EXAM)
    if not ch_hw: return

    # Daily homework reminder
    today_str = date.today().isoformat()
    hw = get_hw(done=0)
    today_hw = [h for h in hw if h.get("due_date","") and h.get("due_date","") <= today_str]
    all_pending = [h for h in hw]

    e = hw_embed(today_hw if today_hw else all_pending[:5],
                 f"🌅 早安！今日待做功課 ({today_str})")
    e.set_footer(text=f"共 {len(hw)} 項待做")
    await ch_hw.send(f"<@{USER_ID}>", embed=e)

    # Exam countdown milestones
    if ch_exam:
        exams = get_exams()
        for ex in exams:
            dl = ex.get("days_left")
            if dl is None: continue
            dl = int(dl)
            if dl in [7, 3, 1]:
                color = 0xff3b30 if dl <= 3 else 0xff9f0a
                ee = discord.Embed(
                    title=f"⏰ 考試倒數 {dl} 天！",
                    description=f"**[{ex['subject']}] {ex.get('title','')}**",
                    color=color
                )
                if ex.get("scope"):
                    ee.add_field(name="範圍", value=ex["scope"])
                ee.add_field(name="日期", value=ex["exam_date"])
                await ch_exam.send(f"<@{USER_ID}>", embed=ee)

@tasks.loop(minutes=1)
async def deadline_reminder():
    """Remind 1 day before and on due day"""
    now = datetime.now().strftime("%H:%M")
    if now != "08:00":
        return
    ch = client.get_channel(CH_HOMEWORK)
    if not ch: return
    today = date.today()
    tmr   = (today + timedelta(days=1)).isoformat()
    hw_tomorrow = [h for h in get_hw(done=0) if h.get("due_date","") == tmr]
    if hw_tomorrow:
        e = hw_embed(hw_tomorrow, "⚠️ 明日截止功課")
        await ch.send(f"<@{USER_ID}>", embed=e)


# ── Message handler (AI channel) ─────────────────────────────────────────────

@client.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.id != CH_AI: return
    if message.author.id != USER_ID: return

    async with message.channel.typing():
        answer = await asyncio.get_event_loop().run_in_executor(
            None, ask_ai, message.content)
    e = discord.Embed(description=answer[:4000], color=0x5856d6)
    await message.reply(embed=e)


# ── Events ────────────────────────────────────────────────────────────────────

@client.event
async def on_ready():
    print(f"[Bot] Logged in as {client.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild)
        synced = await tree.sync(guild=guild)
        print(f"[Bot] Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"[Bot] Sync error: {e}")

    # System notification
    ch = client.get_channel(CH_SYSTEM)
    if ch:
        e = discord.Embed(
            title="✅ SchoolSystem Bot 已上線",
            description=f"版本 v1.3.6 | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            color=0x34c759
        )
        e.add_field(name="指令", value="/hw /today /add /done /exam /stats /ask /study /cycle")
        await ch.send(embed=e)

    daily_reminder.start()
    deadline_reminder.start()


def run_bot():
    if not TOKEN:
        print("[Bot] No DISCORD_TOKEN set, skipping bot startup")
        return
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(client.start(TOKEN))
    except Exception as e:
        print(f"[Bot] Error: {e}")
    finally:
        loop.close()


if __name__ == "__main__":
    run_bot()
