# 系統架構

SchoolSystem 的完整設計文檔。

## 高層架構

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                         │
├──────────────────────┬──────────────────┬───────────────────┤
│   Web UI (iPad)      │  Discord Bot     │   Mobile Browser  │
│   http://IP:8081     │   Slash Commands │   (Optional)      │
└──────────────────────┴──────────────────┴───────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│  Flask API  │ │ Discord.py  │ │ Agent Engine │
│  (main.py)  │ │  (bot.py)   │ │ (agent.py)   │
└─────────────┘ └─────────────┘ └──────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  SQLite DB   │ │ External API │ │   File Sys   │
│ (homework,   │ │ (DeepSeek AI)│ │ (recordings) │
│  exams, log) │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

## 核心模塊

### 1. Flask Backend (main.py)

**責任：**
- HTTP 服務器 + 路由管理
- 用戶身份認證 + 授權
- 數據庫操作 (CRUD)
- RESTful API 端點
- 管理面板

**關鍵函數：**

| 函數 | 用途 |
|------|------|
| `get_db()` | 獲取數據庫連接 (Flask g 對象) |
| `auth(request)` | 驗證 Cookie 認證 |
| `admin_auth(request)` | 驗證管理員密鑰 |
| `log_action()` | 記錄用戶操作 |
| `get_cycle_day()` | 計算當前 Cycle Day |

**API 分組：**

```
/api
├── /today            # 功課端點
├── /hw               # 功課 CRUD
├── /hw/<id>/done     # 標記完成
├── /exams            # 考試管理
├── /stats            # 統計分析
├── /ai
│   ├── /ask          # AI 問答
│   └── /study_plan   # 溫書計劃
├── /whiteboard       # 白板識別
├── /recordings       # 錄音管理
└── /admin            # 管理面板
```

### 2. Discord Bot (bot.py)

**責任：**
- Discord WebSocket 連接
- Slash Commands 註冊 + 處理
- 背景任務 (daily reminders)
- 事件監聽

**架構：**

```python
client = discord.Client()
tree = app_commands.CommandTree(client)

@tree.command(name="...")  # Slash command
async def command_handler(interaction):
    # 處理邏輯
```

**後台任務：**

- `daily_reminder()` - 每天 07:30 發送功課提醒
- `deadline_reminder()` - 每小時檢查截止日期

### 3. AI Agent Engine (agent.py)

**架構 - 代理模式：**

```
┌─────────────────────────────────────┐
│   OrchestratorAgent (路由)          │
│   - 理解用戶意圖                    │
│   - 選擇合適的 SubAgent             │
│   - 整合結果                        │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┬──────────────┐
    │         │         │              │
    ▼         ▼         ▼              ▼
┌────────┐┌──────┐┌─────┐      ┌────────────┐
│AddHW   ││Exam  ││Stats │ ... │CustomAgent │
│Agent   ││Agent ││Agent │     │            │
└────────┘└──────┘└─────┘      └────────────┘
    │         │         │              │
    └─────────┼─────────┴──────────────┘
              │
    ┌─────────▼─────────┐
    │ DeepSeek API      │
    │ (LLM Reasoner)    │
    └───────────────────┘
```

**代理接口：**

```python
class SubAgent:
    def process(self, user_input: str) -> dict:
        """處理用戶請求"""
        # 1. 驗證輸入
        # 2. 準備系統提示
        # 3. 調用 LLM
        # 4. 解析結果
        # 5. 執行操作 (DB 寫入等)
        # 6. 返回響應
        return {
            "answer": "...",
            "action": "...",
            "agent": "..."
        }
```

### 4. 時間表系統 (timetable.py)

**7-day Cycle 模型：**

```
Day 1 (週一)   Day 2 (週二)   ... Day 7 (週日)
08:20-09:00    08:20-09:00         [休息]
09:00-09:40    09:00-09:40
...            ...
16:20-17:00    16:20-17:00
```

**功能：**

- `get_cycle_day()` - 計算當前 Cycle Day (1-7)
- `is_school_day(date)` - 檢查是否學校日期
- `get_timetable(day)` - 獲取特定 day 的課程表

### 5. 錄音系統 (recording.py)

**Flask Blueprint 模塊：**

```python
recording_bp = Blueprint("recording", __name__)

@recording_bp.route("/upload", methods=["POST"])
def upload_recording():
    # 處理音頻上傳
    # 保存到 recordings/ 目錄
    # 更新數據庫
```

## 數據流

### 用戶添加功課流程

```
1. 用戶提交功課 (Web UI / Discord)
   ↓
2. API 路由接收請求
   ├─ Web: POST /api/hw
   └─ Discord: /add 命令
   ↓
3. AI Agent 處理 (如適用)
   ├─ 驗證必要字段
   ├─ 調用 DeepSeek 理解意圖
   └─ 構建結構化數據
   ↓
4. 數據庫插入
   INSERT INTO homeworks (title, subject, ...)
   ↓
5. 返回確認 + 更新 UI
   ├─ Web: 刷新功課列表
   └─ Discord: 發送確認消息
```

### 每日提醒流程

```
1. Background Task Trigger (07:30)
   ↓
2. Discord Bot 定時任務
   daily_reminder.start()
   ↓
3. 查詢數據庫
   SELECT * FROM homeworks WHERE due_date = TODAY
   ↓
4. 過濾重點功課
   - 按優先級排序
   - 按類型分類
   ↓
5. 發送 Discord 嵌入消息
   - Channel: CH_HOMEWORK
   - User: @ 提及用戶
```

## 認證 & 授權

### 認證流程

```
┌─────────────────────────────────────┐
│ 1. 初始訪問 (無認證)                 │
│    http://IP:8081                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 2. 顯示登入頁面                     │
│    要求輸入 SECRET_KEY              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 3. 驗證密鑰                         │
│    if input == SECRET_KEY:          │
│        ✓ 設置 Cookie               │
│    else:                            │
│        ✗ 拒絕訪問                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ 4. Cookie 有效期                    │
│    有效期: 30 天                     │
│    自動更新: 每次請求               │
│    過期後: 重新登入                 │
└─────────────────────────────────────┘
```

### 授權等級

```
公開訪問 (auth = False)
├─ GET /health
└─ GET / (若已登入)

認證訪問 (auth = True)
├─ GET /api/...
├─ POST /api/...
└─ GET /admin (基本)

管理員訪問 (admin_auth = True)
├─ GET /admin
├─ POST /admin/update
└─ POST /admin/settings
```

## 部署架構

### 目標環境: Termux (Android)

```
Android 設備
├─ Termux 應用
│  └─ Linux 環境
│     ├─ Python 3.10+
│     ├─ SQLite 3
│     └─ watchdog (自動重啟)
│
├─ schoolsystem.db (本地)
├─ recordings/ (媒體)
└─ logs/ (日誌)

iPad (學校 WiFi)
│
└─ VPN 連接
   └─ http://ANDROID_IP:8081
      ├─ Web UI
      ├─ API
      └─ WebSocket (Discord 連接)
```

### Watchdog 機制

```
start.sh (bash script)
│
├─ 監控 main.py 進程
├─ 檢查進程健康狀態
└─ 若崩潰:
   ├─ 記錄日誌
   ├─ 等待 3 秒
   └─ 自動重啟
```

## 性能考量

### 優化策略

| 優化項 | 方法 |
|--------|------|
| 數據庫查詢 | 使用索引 + 緩存 |
| API 響應 | 異步處理 + 分頁 |
| 前端 | JavaScript 緩存 + 最小化 |
| 圖像 | 壓縮 + 延遲加載 |

### 資源限制

```python
# 最大上傳大小: 100 MB
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

# 日誌保留: 最新 1000 條記錄
LOGS_RETENTION = 1000

# API 超時: 30 秒
TIMEOUT = 30
```

## 錯誤處理

### 統一錯誤響應

```python
{
    "error": "error_code",
    "message": "Human readable message",
    "details": {...}  # 可選
}
```

### HTTP 狀態碼

```
200 OK          - 成功
201 Created     - 新建資源
400 Bad Request - 無效輸入
401 Unauthorized- 未認證
403 Forbidden   - 無權限
404 Not Found   - 資源不存在
500 Server Error- 服務器錯誤
503 Service Unavailable - 服務不可用
```

## 安全考量

1. **密鑰管理**
   - 使用環境變數儲存敏感信息
   - 不將密鑰提交到 git

2. **數據驗證**
   - 驗證所有用戶輸入
   - SQL 注入防護 (使用參數化查詢)

3. **CORS**
   - 僅允許信任的源
   - 生產環境配置必要

4. **日誌安全**
   - 不記錄密碼或 API 密鑰
   - 定期清理日誌

