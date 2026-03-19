# Changelog

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
