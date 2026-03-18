# 開發指南

詳細的開發工作流和項目結構說明。

## 項目結構

```
SchoolSystem/
├── main.py              # Flask 後端 + 主 API 路由
├── bot.py               # Discord Bot + Slash Commands
├── agent.py             # AI Agent 編排引擎
├── study_plan.py        # 溫書計劃生成器
├── timetable.py         # 7-day Cycle 時間表數據
├── recording.py         # 錄音 Blueprint 模塊
├── ui.py                # 前端 HTML/CSS/JS（嵌入式）
│
├── docs/                # 文檔
│   ├── DEVELOPMENT.md   # 本文件
│   ├── ARCHITECTURE.md  # 系統設計
│   └── API.md           # API 參考
│
├── tests/               # 測試
│   ├── __init__.py
│   ├── conftest.py      # pytest fixtures
│   ├── test_main.py     # API 測試
│   ├── test_homework.py # 功課邏輯測試
│   └── test_agent.py    # AI Agent 測試
│
├── requirements.txt     # 生產依賴
├── requirements-dev.txt # 開發依賴
├── pyproject.toml       # 項目配置 + 工具設定
├── .editorconfig        # 編輯器規範
├── .pre-commit-config.yaml  # Pre-commit 鉤子
├── .env.example         # 環境變數模板
│
└── .github/
    └── workflows/       # GitHub Actions
        ├── lint.yml     # 代碼風格檢查
        ├── test.yml     # 自動化測試
        └── release.yml  # 版本發佈
```

## 本地開發

### 前置要求

- Python 3.10+
- pip + venv
- git

### 快速啟動

```bash
# 1. Clone 和進入目錄
git clone https://github.com/SchoolSystemYiu/SchoolSystem.git
cd SchoolSystem

# 2. 創建虛擬環境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate (Windows)

# 3. 安裝依賴
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 設定環境變數
cp .env.example .env
# 編輯 .env 填入 Discord Token, API Keys 等

# 5. 運行應用
python main.py

# 應用將運行在 http://localhost:8081
```

### 代碼風格檢查

在提交前運行：

```bash
# 自動格式化代碼
black .

# 檢查並修復 import 順序
isort .

# 靜態分析檢查
flake8 .

# 或使用 pre-commit hooks（會在 git commit 時自動運行）
pre-commit run --all-files
```

## 項目架構

### Flask 應用（main.py）

**路由分類：**

| 路由 | 功能 | 認證 |
|------|------|------|
| `GET /health` | 系統健康檢查 | 否 |
| `GET /` | 網頁 UI | Cookie |
| `GET /admin` | 管理面板 | 密鑰 + Cookie |
| `POST /api/hw` | 新增功課 | Cookie |
| `GET /api/today` | 今日功課 + Cycle Day | Cookie |
| `POST /api/ai/ask` | AI 問答 | Cookie + API Key |
| `GET /api/logs` | 訪問日誌 | 管理員 |

**身份認證流程：**

1. 用戶輸入密鑰 → 驗證 `SECRET_KEY`
2. 設置 Cookie (有效 30 天)
3. 後續請求通過 Cookie 認證

### Discord Bot（bot.py）

**Slash Commands：**

| 命令 | 功能 |
|------|------|
| `/hw` | 顯示所有待做功課 |
| `/today` | 今日截止功課 |
| `/add` | 新增功課對話 |
| `/done` | 標記功課完成 |
| `/exam` | 考試列表 |
| `/stats` | 統計信息 |
| `/ask` | AI 對話 |
| `/study` | 生成溫書計劃 |
| `/cycle` | 當前 Cycle Day |

**後台任務：**

- `daily_reminder()` - 每日 07:30 提醒
- `deadline_reminder()` - 每小時檢查截止日期

### AI Agent 系統（agent.py）

**代理架構：**

```
OrchestratorAgent (main)
├── AddHWAgent         # 理解並新增功課
├── ExamAnalyzer       # 分析考試日期
├── StudyPlanner       # 生成溫書計劃
└── StatsAnalyzer      # 統計分析
```

**流程：**

1. 用戶輸入 (自然語言)
2. Orchestrator 分析意圖
3. 路由到相應 SubAgent
4. 調用 DeepSeek API (可選)
5. 返回結構化結果

## 數據庫

### SQLite 架構

```sql
-- 功課表
CREATE TABLE homeworks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    subject TEXT,
    hw_type TEXT,  -- 功課/小測/考試等
    done BOOLEAN,
    priority TEXT,  -- 高/中/低
    due_date TEXT,  -- ISO format (YYYY-MM-DD)
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 考試表
CREATE TABLE exams (
    id INTEGER PRIMARY KEY,
    title TEXT,
    exam_date TEXT,  -- ISO format
    countdown INTEGER,  -- 天數
    created_at TIMESTAMP
);

-- 訪問日誌表
CREATE TABLE access_log (
    id INTEGER PRIMARY KEY,
    ip TEXT,
    action TEXT,
    detail TEXT,
    timestamp TIMESTAMP
);

-- 錄音表
CREATE TABLE recordings (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    subject TEXT,
    date TEXT,
    duration INTEGER,  -- 秒
    file_path TEXT,
    created_at TIMESTAMP
);
```

## 測試

### 運行測試

```bash
# 運行所有測試
pytest tests/

# 運行特定測試文件
pytest tests/test_main.py

# 運行帶覆蓋率報告
pytest tests/ --cov=. --cov-report=html

# 生成覆蓋率 HTML 報告
# 打開 htmlcov/index.html
```

### 編寫測試

使用 pytest + fixtures：

```python
# tests/test_example.py
import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
```

## 環境變數

參見 `.env.example`：

```ini
# 認證
SECRET_KEY=your-secret-key
ADMIN_KEY=your-admin-key

# Discord Bot
DISCORD_TOKEN=your-bot-token
DISCORD_GUILD_ID=your-server-id
DISCORD_CH_HOMEWORK=homework-channel-id
DISCORD_CH_AI=ai-channel-id
DISCORD_CH_SYSTEM=system-channel-id
DISCORD_CH_EXAM=exam-channel-id
DISCORD_USER_ID=your-user-id

# AI API
DEEPSEEK_API_KEY=your-deepseek-key  # 可選

# 服務器
PORT=8081
BIND_HOST=0.0.0.0
CYCLE_START_DATE=2025-09-02
DAILY_REMINDER_TIME=07:30
```

## 常見任務

### 添加新的 API 路由

```python
@app.route("/api/newfeature", methods=["GET"])
def new_feature():
    if not auth(request):
        return jsonify({"error": "unauthorized"}), 401

    log_action(request, "new_feature", "accessing new feature")

    db = get_db()
    # 實現邏輯
    return jsonify({"status": "success"})
```

### 添加新的 Slash Command

```python
@tree.command(name="example", description="Example command")
async def example(interaction: discord.Interaction):
    await interaction.response.defer()
    # 實現邏輯
    await interaction.followup.send("Response")
```

### 添加新的 AI Agent

1. 在 `agent.py` 中實現 SubAgent 類
2. 在 Orchestrator 中註冊
3. 添加相應的路由或命令

## 問題排查

### Port 已被佔用

```bash
# Kill 進程（macOS/Linux）
lsof -ti:8081 | xargs kill -9

# Windows
netstat -ano | findstr :8081
taskkill /PID <PID> /F
```

### 環境變數未讀取

確保 `.env` 在項目根目錄，並在程序啟動時調用 `load_dotenv()`。

### Discord Bot 無響應

1. 檢查 TOKEN 是否正確
2. 確認 Bot 有應用程序命令權限
3. 查看 Discord 開發者門戶中的 OAuth 範圍

## 貢獻工作流

參見 [CONTRIBUTING.md](../CONTRIBUTING.md)

