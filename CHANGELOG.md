# Changelog

## [2.0.0-alpha.11] - 2026-03-19 🔥 CRITICAL FIX
### 修復
- 🐛 **解決 JavaScript 模塊缓存問題** - 前端按鈕無法加載
  - 清除 Python bytecode 缓存防止舊版本加載
  - 確保 ui.py 腳本標籤在 HTML body 之前加載
  - script tag 現在正確位置在 `</style>` 和 `</head>` 之間
  - 所有導航按鈕、深色模式、功能完全恢復

### 影響
- ✅ 前端完全恢復正常運作
- ✅ 所有 onclick 處理器正確引用函數
- ✅ 錯誤處理系統正常顯示 JavaScript 錯誤

---

## [2.0.0-alpha.10-hotfix.1] - 2026-03-19 🔥 HOTFIX
### 新增
- 🚀 **現代化更新系統** - 全新設計的版本管理
  - 版本渠道選擇：Alpha（最新） / Beta（穩定） / Stable
  - 改進的 Admin Panel 更新 UI
  - 更清晰的版本信息顯示
  - 更好的錯誤報告和詳細信息

### 修復
- 🐛 **修復前端 JavaScript 錯誤** - "go is not defined"
  - HTML 按鈕 onclick 屬性在腳本定義前被解析
  - 移動核心函數定義到腳本頂部
  - 確保 go(), goB(), toggleDark() 在頁面加載時可用

### 更新
- 📝 版本號更新至 2.0.0-alpha.10-hotfix.1
- 🎨 改進 Admin Panel 樣式和互動

### 影響
- ✅ 所有導航按鈕（主頁、時間表、功課等）現在正常工作
- ✅ 深色模式切換按鈕恢復正常
- ✅ 可以選擇 Alpha 版本接收最新功能
- ✅ 完整的 Git reset 更新系統

---

## [2.0.0-alpha.10] - 2026-03-19 🧪 ALPHA
### 新增
- ⚡ **Wake-On-LAN (WOL) 整合** - 支援 ESP8266 遠程喚醒 PC
  - Admin Panel 快速操作按鈕 (⚡ 開機 PC)
  - HTTP API 端點 `/admin/wol`
  - 設定 `ESP8266_IP` 環境變數
  - JavaScript 前端集成，實時反饋

- 🔄 **完整 Git 重置更新系統** - 真正的「一鍵完整更新」
  - 用 `git fetch + git reset --hard` 替換不完整的 HTTP 備用方案
  - **更新所有文件**：main.py、docs、.github、templates、所有配置文件
  - 移除不可靠的多鏡像 HTTP 下載
  - 所有 shell 腳本自動設定可執行權限
  - 更好的錯誤報告和反饋訊息

### 技術細節
- 透過 ESP8266 HTTP 服務轉發 Magic Packet
- 支援 UDP 廣播喚醒 (Port 9)
- Admin 認證保護，防止濫用
- 更新系統：完整 Git Workflow (Fetch → Reset → Validate → Restart)

---

## [2.0.0-alpha.1] - 2026-03-18 🧪 ALPHA
### ⚠️ Alpha Release — 測試版本，可能有 Bug

### 新增
- 🤖 AI 溫書計劃生成 (考試日期 + 空堂 + 假期分析)
- ⚡ 今日優先事項 (唔需要 AI Key)
- 🎯 Discord Bot Slash Commands (9個指令)
- 🔄 Watchdog 自動重啟系統
- 📷 白板拍照 AI 識別功課
- 📋 考試 & 小測統一管理

### 已知問題 (Known Issues)
- Discord Bot event loop 待測試
- 白板 AI 識別需要 DeepSeek Vision (部分模型不支援)
- 更新系統依賴 git 初始化

### 版本標籤說明
- `alpha` — 新功能測試中，可能有 Bug
- `beta` — 功能完整，修復緊要 Bug
- `stable` — 穩定版本，可放心使用
- `hotfix` — 緊急修復

---

## [2.0.0-alpha.8] - 2026-03-18 🧪 Alpha
### 更新
- update system包括start.sh+chmod，README badge修復，CHANGELOG自動更新，watchdog自我更新

---

所有版本更新記錄。格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

版本號格式：`MAJOR.MINOR.PATCH[-hotfix.N]`
- `MAJOR` — 重大架構變更
- `MINOR` — 新功能
- `PATCH` — Bug 修復
- `hotfix.N` — 緊急修復 (不改 PATCH 號)

---

## [2.0.0-alpha.9] - 2026-03-18 🧪 ALPHA
### 更新
- update system includes all files + self-updating watchdog, README badge fixed (shields.io double-dash encoding), CHANGELOG auto-update on version bump

---

## [1.3.8] - 2026-03-18
### 新增
- `start.sh` Watchdog 腳本，crash 後 3 秒自動重啟
- `termux-boot/` Termux:Boot 開機自啟支援
- Discord Bot (`bot.py`) Slash Commands + 每日提醒

### 修復
- 移除所有 `os.execv`，改用 SIGTERM + watchdog 重啟
- Admin Panel 更新後服務唔會死

---

## [1.3.7] - 2026-03-18
### 新增
- Discord Bot 完整實現
- Slash Commands: `/hw` `/today` `/add` `/done` `/exam` `/stats` `/ask` `/study` `/cycle`
- 每日早上提醒、截止前1天提醒、考試倒數里程碑

---

## [1.3.6] - 2026-03-18
### 修復
- 更新系統改用 `git pull` 為主要方法
- HTTP 下載改用多鏡像備用 (jsdelivr → raw.githubusercontent → github raw)
- 更新失敗時顯示詳細錯誤原因

---

## [1.3.5] - 2026-03-18
### 修復 (Hotfix)
- JS syntax error: `aiStudyPlan` 函數內字串含 literal newline
- `go is not defined` 錯誤

---

## [1.3.4] - 2026-03-18
### 修復
- `GH_RAW` 變數從未定義 (根本原因)
- 更新系統加入 jsdelivr CDN 備用

---

## [1.3.3] - 2026-03-18
### 新增
- 管理員介面重新設計 (4 tabs: 狀態/更新/日誌/設定)
- 全局 JS 錯誤橫幅 (底部顯示，可複製)
- Admin Panel 可查看訪問日誌 + log.txt
- 更新系統顯示成功/失敗文件清單

### 變更
- 白板移到「加功課」頁面右上角

---

## [1.3.2] - 2026-03-18
### 修復 (Hotfix)
- 移除重複 `ai_ask` route，導致 Flask 啟動 crash

---

## [1.3.1] - 2026-03-18
### 新增
- 白板拍照上載 + AI 識別功課
- 考試 & 小測合一 tab (Segment 切換)
- Chrome Android 底部 tab bar 修復

---

## [1.3.0] - 2026-03-18
### 新增
- AI Agent 架構 (OrchestratorAgent)
- `/api/whiteboard/upload` endpoint

---

## [1.2.0] - 2026-03-18
### 新增
- 錄音功能 (`recording.py` Blueprint)
- 完成功課撤銷 (4秒 undo)
- 表單清除按鈕
- 管理員介面更新功能

---

## [1.1.0] - 2026-03-18
### 新增
- Cycle Day 計算 (7日滾動制)
- 完整課程時間表 Day 1-7
- AI 助手介面 (DeepSeek Reasoner)
- 管理員在線編輯 .env

---

## [1.0.0] - 2026-03-17
### 新增
- 基礎功課 CRUD
- 考試倒數管理
- 登入/Cookie 認證
- SQLite 數據庫
- 統計頁面
