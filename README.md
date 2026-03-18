# 📚 SchoolSystem

> 個人學習管理系統 — 專為香港 DSE 學生設計

![Version](https://img.shields.io/badge/version-2.0.0--alpha.9-5856d6?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-3.1-lightgrey)
![Discord](https://img.shields.io/badge/discord.py-2.4-5865f2)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-actively%20maintained-brightgreen)

---

## ✨ 核心功能

| 功能 | 說明 |
|------|------|
| 📝 **功課管理** | 記錄功課、小測、默書、實驗，支援優先級、截止日期、撤銷 |
| 📋 **課程時間表** | 7日 Cycle 制度，自動顯示今日係 Day 幾，當堂高亮 |
| 📅 **考試 & 小測** | 統一管理，自動倒數，里程碑提醒 |
| 📷 **白板識別** | AI 自動識別白板功課內容，一鍵加入功課表 |
| 🎙️ **錄音存檔** | 錄製課堂筆記，支援多種音頻格式 |
| 🤖 **AI 助手** | DeepSeek Reasoner 驅動，溫書計劃、功課建議 |
| 💬 **Discord Bot** | Slash Commands、每日提醒、考試倒數推送 |
| 📊 **統計分析** | 完成率、各科功課量、逾期記錄 |
| ⚙️ **管理員面板** | 自動更新、在線編輯設定、日誌查看 |
| 🔄 **自動重啟** | Watchdog 監控，Crash 後 3 秒自動恢復 |

---

## 🚀 快速開始

### 系統要求

- **硬件**：Android 手機（推薦 Redmi Note 12）
- **軟件**：Termux + Python 3.10+
- **網絡**：家中 Wi-Fi 或學校 VPN

### 安裝步驟

#### 1️⃣ 在 Termux 中安裝依賴

```bash
pkg install python git -y
git clone https://github.com/SchoolSystem/SchoolSystem.git
cd SchoolSystem
```

#### 2️⃣ 安裝 Python 套件

```bash
# 使用 requirements.txt（推薦）
pip install -r requirements.txt

# 或手動安裝
pip install Flask discord.py python-dotenv requests
```

#### 3️⃣ 設定環境變數

```bash
cp .env.example .env
nano .env  # 編輯密鑰、API 密鑰等
```

**環境變數說明** - 見 [.env.example](.env.example)

#### 4️⃣ 啟動應用

```bash
# 使用 Watchdog（推薦，會自動重啟）
nohup bash start.sh > /dev/null 2>&1 &
termux-wake-lock

# 或直接運行
python main.py
```

應用將運行在 `http://YOUR_DEVICE_IP:8081`

---

## 📖 完整文檔

| 文檔 | 說明 |
|------|------|
| 🗺️ [項目路線圖](ROADMAP.md) | 功能優先級、里程碑、Kanban 看板 |
| 📊 [項目管理指南](PROJECT_MANAGEMENT.md) | GitHub 工作流、Issue/PR 流程 |
| 🏗️ [系統架構](docs/ARCHITECTURE.md) | 高層設計、模塊說明、數據流 |
| 🔌 [API 參考](docs/API.md) | 完整 REST API 端點、請求/響應示例 |
| 👨‍💻 [開發指南](docs/DEVELOPMENT.md) | 本地開發設置、代碼風格、測試指南 |
| 🤝 [貢獻指南](CONTRIBUTING.md) | PR 流程、代碼規範、報告 Bug |
| 📜 [行為準則](CODE_OF_CONDUCT.md) | 社區指南、行為標準 |
| 🎯 [類型提示指南](docs/TYPE_HINTS_GUIDE.md) | Type hints、Docstrings 規範 |

---

## 📱 使用方法

### Web UI（iPad / 瀏覽器）

```
訪問：http://YOUR_DEVICE_IP:8081
登入：輸入 SECRET_KEY
功能：
  - 功課管理（新增、完成、刪除）
  - 查看時間表 + Cycle Day
  - 統計分析
  - 管理員面板（更新、設定、日誌）
```

### Discord Bot（Discord 伺服器）

```
/hw              → 顯示所有待做功課
/today           → 今日截止功課
/add             → 新增功課（對話模式）
/done <id>       → 標記功課完成
/exam            → 考試列表
/stats           → 統計信息
/ask <問題>      → AI 問答
/study <天數>    → 生成溫書計劃
/cycle           → 今日 Day 幾 + 課表
```

### REST API（程式整合）

```bash
# 取得今日功課
curl http://YOUR_DEVICE_IP:8081/api/today

# 新增功課
curl -X POST http://YOUR_DEVICE_IP:8081/api/hw \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chemistry Lab",
    "subject": "CHEM",
    "hw_type": "實驗",
    "due_date": "2025-03-25",
    "priority": "高"
  }'

# 完整 API 文檔見 docs/API.md
```

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────┐
│   iPad / Browser / Discord          │
│   (Multiple User Interfaces)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Flask Backend (main.py)           │
│   - REST API                        │
│   - Authentication                  │
│   - Database Operations             │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌─────────┐
│SQLite  │ │AI Agent│ │Recording│
│Database│ │(Bot)   │ │Module   │
└────────┘ └────────┘ └─────────┘
```

詳見 [系統架構文檔](docs/ARCHITECTURE.md)

---

## 🛠️ 開發

### 開發環境設置

```bash
# 建立虛擬環境
python -m venv venv
source venv/bin/activate

# 安裝開發工具
pip install -r requirements-dev.txt

# 安裝 pre-commit hooks
pre-commit install

# 運行代碼風格檢查
black .
flake8 .
isort .

# 運行測試
pytest tests/ -v --cov=.
```

### 代碼風格

- **Python**: PEP 8 (使用 Black + isort 自動格式化)
- **Import**: 標準庫 → 第三方 → 本地 (PEP 8 順序)
- **類型提示**: 推薦（見 [類型提示指南](docs/TYPE_HINTS_GUIDE.md)）
- **Docstrings**: Google 風格

### 貢獻流程

1. Fork 項目
2. 創建 feature 分支 (`git checkout -b feature/xyz`)
3. 提交變更 (`git commit -m "feat(scope): description"`)
4. 推送到分支 (`git push origin feature/xyz`)
5. 開啟 Pull Request

詳見 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📊 項目狀態

### 最新版本：2.0.0-alpha.1

| 組件 | 狀態 | 說明 |
|------|------|------|
| 核心功能 | ✅ 完成 | 功課、時間表、考試管理 |
| Discord Bot | ✅ 完成 | 所有 Slash Commands |
| AI 助手 | ✅ 完成 | DeepSeek 整合 |
| 標準化 | ✅ 完成 | 依賴管理、代碼風格、CI/CD |
| 文檔 | ✅ 完成 | API、架構、開發指南 |
| 測試 | 🟨 進行中 | 基礎框架完成，需增加覆蓋率 |
| 類型提示 | 🟨 進行中 | 指南完成，待逐步實施 |

見 [TODO.md](TODO.md) 了解未來計劃

---

## 🔄 更新

### 使用 Admin Panel（推薦）

1. 訪問 `http://YOUR_DEVICE_IP:8081/admin`
2. 進入「更新」標籤
3. 點擊「檢查更新」
4. 點擊「立即更新」
5. 系統自動 `git pull` + 重啟

### 手動更新

```bash
cd ~/SchoolSystem
git pull origin main
# Watchdog 會自動重啟，或手動：
pkill -f "python main.py" && nohup bash start.sh > /dev/null 2>&1 &
```

---

## 🔒 安全

- ✅ `.env` 已加入 `.gitignore`，敏感信息不上傳
- ✅ Cookie 認證，30 天有效期
- ✅ 管理員功能需要獨立 Admin Key
- ✅ 所有請求記錄訪問日誌
- ✅ SQL 查詢使用參數化防止注入
- ⚠️ 建議 HTTPS 用於遠程訪問

---

## 📋 版本歷史

見 [CHANGELOG.md](CHANGELOG.md) 了解完整版本歷史

### 主要里程碑

| 版本 | 日期 | 亮點 |
|------|------|------|
| v2.0.0 (alpha) | 2025-03 | 項目標準化、完整文檔、測試框架 |
| v1.3.8 | 2025-02 | Watchdog 自動重啟 |
| v1.3.0 | 2025-01 | AI Agent 架構 |
| v1.0.0 | 2024-12 | MVP 發佈 |

---

## 💡 常見問題

### Q: 如何在學校 iPad 訪問？
**A:** 使用 L2TP VPN 連接到家中網絡，然後訪問 `http://YOUR_DEVICE_IP:8081`

### Q: AI 功能不工作？
**A:** 檢查是否設置了 `DEEPSEEK_API_KEY`（可選）。若不設置，AI 功能將被禁用。

### Q: 如何備份功課數據？
**A:** 複製 `schoolsystem.db` 文件。Admin Panel 也支持導出日誌。

### Q: 可以在多個設備上使用嗎？
**A:** 可以。多個設備可以同時連接到同一個伺服器實例。

更多問題見 [CONTRIBUTING.md](CONTRIBUTING.md#問題或需要幫助)

---

## 🤝 貢獻

感謝所有貢獻者！

- 📝 報告 Bug：[GitHub Issues](https://github.com/SchoolSystem/issues)
- 💬 建議功能：[GitHub Discussions](https://github.com/SchoolSystem/discussions)
- 🔀 提交 PR：見 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License © 2026

見 [LICENSE](LICENSE) 了解詳細許可條款

---

## 🙏 鳴謝

感謝香港 DSE 學生社區的反饋和支持。

特別感謝：
- **Flask** - Web 框架
- **discord.py** - Discord 集成
- **DeepSeek** - AI 功能
- **SQLite** - 數據儲存

---

## 📧 聯繫

- 📌 GitHub: [Project Repository](https://github.com/SchoolSystem)
- 📚 Project: [SchoolSystem](https://github.com/SchoolSystem)
- 💬 Issues: [Bug Reports & Features](https://github.com/SchoolSystem/issues)

---

<div align="center">

**Built with ❤️ for DSE students in Hong Kong 🇭🇰**

[⬆ 返回頂部](#-schoolsystem)

</div>
