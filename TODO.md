# 📋 TODO & Roadmap

> 追蹤所有計劃功能、已知問題、改進方向

---

## 🔴 緊急 (本版本修復)

- [ ] Discord Bot event loop 測試同修復
- [ ] 白板 AI 識別準確率提升
- [ ] 更新系統穩定性測試

---

## 🟡 v2.0.0-beta 目標

### Discord Bot 完整功能
- [ ] `/hw` 分頁顯示（超過10項）
- [ ] `/add` 加入截止日期 autocomplete
- [ ] `/done` 顯示功課列表選擇
- [ ] 每日提醒訊息美化（Embed 圖表）
- [ ] 考試倒數自動 DM 提醒
- [ ] Bot 離線時自動重連

### AI Agent 系統
- [ ] OrchestratorAgent 完善
- [ ] HomeworkAgent（自動識別功課優先級）
- [ ] StudyAgent（動態調整溫書計劃）
- [ ] TimetableAgent（空堂識別）

### 溫書計劃
- [ ] 匯出 PDF 格式
- [ ] 儲存歷史計劃記錄
- [ ] 根據實際完成情況動態調整

---

## 🟢 v2.1.0 計劃

### 統計頁面完善
- [ ] 成績追蹤（小測/考試成績記錄）
- [ ] 溫書時數記錄（計時器功能）
- [ ] 每週學習報告
- [ ] 科目完成率圖表

### 化學 PDF 自動解析
- [ ] Google Classroom PDF 下載
- [ ] DeepSeek Vision 解析化學功課
- [ ] 自動加入功課表（剔除已做）
- [ ] 識別刪除線（已完成功課）

---

## 🔵 v2.2.0 未來功能

- [ ] 多用戶支援
- [ ] 匯出/匯入數據庫
- [ ] 功課提醒 Push Notification
- [ ] Widget（iOS 主畫面）
- [ ] Siri Shortcut 整合
- [ ] Apple Watch 支援

---

## ✅ 已完成

- [x] 基礎功課 CRUD (v1.0.0)
- [x] 考試倒數管理 (v1.0.0)
- [x] Cycle Day 計算 7日制 (v1.1.0)
- [x] 課程時間表 Day 1-7 (v1.1.0)
- [x] AI 助手基礎 (v1.1.0)
- [x] 錄音存檔 (v1.2.0)
- [x] 完成撤銷功能 (v1.2.0)
- [x] 白板拍照上載 (v1.3.1)
- [x] 考試+小測合一 tab (v1.3.1)
- [x] Chrome 底部 tab bar 修復 (v1.3.1)
- [x] 管理員介面重設計 (v1.3.3)
- [x] 全局錯誤橫幅 (v1.3.3)
- [x] 更新系統 git pull 優先 (v1.3.6)
- [x] Watchdog 自動重啟 (v1.3.8)
- [x] Discord Bot 基礎 9 指令 (v1.3.7)
- [x] Git 歷史私隱清除 (v1.3.8)
- [x] AI 溫書計劃（考試+空堂+假期）(v2.0.0)
- [x] 今日優先事項（無需 AI Key）(v2.0.0)

---

## 🐛 已知 Bug

| Bug | 嚴重程度 | 狀態 |
|-----|---------|------|
| Discord Bot 首次啟動可能 event loop 衝突 | 中 | 調查中 |
| 白板識別需要 DeepSeek Vision 模型 | 低 | 已知限制 |
| 統測期間 Cycle Day 計算可能不準 | 低 | 待確認 |

---

*最後更新：2026-03-18*
