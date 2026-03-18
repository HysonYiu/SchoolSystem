# 📚 SchoolSystem

> 個人學習管理系統 — 專為香港 DSE 學生設計

![Version](https://img.shields.io/badge/version-1.3.8-5856d6)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Flask](https://img.shields.io/badge/flask-3.1-lightgrey)
![Discord](https://img.shields.io/badge/discord-bot-5865f2)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ 功能

| 功能 | 說明 |
|------|------|
| 📝 功課管理 | 記錄功課、小測、默書、實驗，支援優先級、截止日期、撤銷 |
| 📋 課程時間表 | 7日 Cycle 制度，自動顯示今日係 Day 幾，當堂高亮 |
| 📅 考試 & 小測 | 統一管理，自動倒數，里程碑提醒 |
| 📷 白板拍照 | AI 自動識別白板功課內容，一撳加入功課表 |
| 🎙️ 錄音存檔 | 錄製課堂筆記，iOS/Android 原生錄音支援 |
| 🤖 AI 助手 | DeepSeek Reasoner 驅動，溫書計劃、功課建議 |
| 🤖 Discord Bot | Slash Commands、每日提醒、考試倒數推送 |
| 📊 統計分析 | 完成率、各科功課量、逾期記錄 |
| ⚙️ 管理員介面 | 自動更新、在線編輯設定、日誌查看 |
| 🔄 Watchdog | 自動重啟，crash 後 3 秒恢復，Admin Panel 一鍵更新 |

---

## 🏗️ 架構

```
Redmi Note 12 (Termux)
├── start.sh           ← Watchdog (自動重啟)
├── main.py            ← Flask 後端 + API
├── bot.py             ← Discord Bot
├── ui.py              ← 前端 HTML/CSS/JS
├── timetable.py       ← 課程表 (Day 1-7)
├── recording.py       ← 錄音 Blueprint
├── .env               ← 密鑰設定 (不上傳)
└── schoolsystem.db    ← SQLite 數據庫

iPad (學校 Wi-Fi + L2TP VPN)
    ↓
http://YOUR_DEVICE_IP:8081
```

---

## 🚀 安裝

### 需要環境
- Android 手機 + Termux
- Python 3.10+

### 步驟

```bash
# 1. 安裝依賴
pkg install python git -y
pip install flask discord.py requests python-dotenv --break-system-packages

# 2. Clone
git clone https://github.com/SchoolSystemYiu/SchoolSystem.git
cd SchoolSystem

# 3. 設定環境變數
cp .env.example .env
nano .env

# 4. 啟動 (watchdog 模式)
nohup bash start.sh > /dev/null 2>&1 &
termux-wake-lock
```

---

## ⚙️ 設定 (.env)

```ini
SECRET_KEY=           # 登入密鑰
ADMIN_KEY=            # 管理員密鑰
DISCORD_TOKEN=        # Discord Bot Token
DISCORD_GUILD_ID=     # Discord Server ID
DISCORD_CH_HOMEWORK=  # 功課提醒 Channel ID
DISCORD_CH_AI=        # AI 對話 Channel ID
DISCORD_CH_SYSTEM=    # 系統通知 Channel ID
DISCORD_CH_EXAM=      # 考試倒數 Channel ID
DISCORD_USER_ID=      # 你的 Discord User ID
DEEPSEEK_API_KEY=     # AI 功能 (可選)
PORT=8081
BIND_HOST=0.0.0.0
DAILY_REMINDER_TIME=07:30
CYCLE_START_DATE=2025-09-02
```

---

## 📱 存取

| 裝置 | 方法 |
|------|------|
| 屋企 Wi-Fi | `http://YOUR_DEVICE_IP:8081` |
| 學校 iPad | L2TP VPN → 同上 |
| 管理員 | `http://YOUR_DEVICE_IP:8081/admin` |

---

## 🔄 更新

**Admin Panel（推薦）：**
`/admin` → 更新 tab → 「檢查更新」→「立即更新」→ 自動 git pull + watchdog 重啟

**手動：**
```bash
cd ~/SchoolSystem
git pull origin main
# watchdog 會自動重啟，或手動：
pkill -f "python main.py" && nohup bash start.sh > /dev/null 2>&1 &
```

---

## 🤖 Discord 指令

| 指令 | 功能 |
|------|------|
| `/hw` | 全部待做功課 |
| `/today` | 今日截止功課 |
| `/add` | 加入功課 |
| `/done` | 標記完成 |
| `/exam` | 考試列表 |
| `/stats` | 統計 |
| `/ask` | 問 AI |
| `/study` | 生成溫書計劃 |
| `/cycle` | 今日 Day 幾 + 課表 |

---

## 📁 API

```
GET  /health                    → 系統狀態
GET  /api/today                 → 今日功課 + Cycle Day
GET  /api/cycle                 → Cycle Day 資訊
GET  /api/timetable?day=N       → 課程表
GET  /api/hw                    → 功課列表
POST /api/hw                    → 加功課
POST /api/hw/<id>/done          → 標記完成
POST /api/hw/<id>/undone        → 撤銷完成
GET  /api/exams                 → 考試列表
GET  /api/stats                 → 統計
POST /api/ai/ask                → AI 問答
POST /api/ai/study_plan         → AI 溫書計劃
POST /api/whiteboard/upload     → 白板上載 + AI 識別
GET  /api/recordings            → 錄音列表
POST /api/recordings/upload     → 上載錄音
GET  /admin                     → 管理員介面
GET  /admin/check_update        → 檢查更新
GET  /admin/update              → 執行更新
```

---

## 📋 版本歷史

| 版本 | 更新內容 |
|------|---------|
| v1.3.8 | Watchdog 自動重啟，移除 os.execv，Termux:Boot 支援 |
| v1.3.7 | Discord Bot，Slash Commands，每日提醒 |
| v1.3.6 | 更新系統 git pull 優先，multi-mirror 備用 |
| v1.3.5 | JS syntax fix，aiStudyPlan 修復 |
| v1.3.4 | GH_RAW 修復，更新系統多鏡像 |
| v1.3.3 | 管理員介面重做，錯誤橫幅，日誌查看 |
| v1.3.2 | 移除重複 ai_ask route |
| v1.3.1 | 白板上載，考試小測合一 tab，Chrome 底部 bar |
| v1.3.0 | AI Agent 架構 |
| v1.2.0 | 錄音，撤銷，管理員更新 |
| v1.1.0 | Cycle Day，時間表，AI 助手 |
| v1.0.0 | 基礎功課管理，考試倒數 |

---

## 🔒 安全

- `.env` 已加入 `.gitignore`，密鑰唔會上傳
- Cookie 認證，30 天有效
- 管理員功能需要獨立 Admin Key
- 訪問日誌記錄所有請求

---

## 📄 License

MIT License © 2026 [SchoolSystemYiu](https://github.com/SchoolSystemYiu)

---

<div align="center">
  <sub>Built for DSE students in Hong Kong 🇭🇰</sub>
</div>
