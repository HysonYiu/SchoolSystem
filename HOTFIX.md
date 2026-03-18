# Hotfix 指南

## 何時用 Hotfix？

- 嚴重 bug 導致服務無法啟動
- JS 錯誤導致前端完全無法使用
- 安全漏洞

## 版本號規則

```
正常更新：v1.3.8 → v1.3.9
Hotfix：  v1.3.8 → v1.3.8-hotfix.1 → v1.3.8-hotfix.2
```

## Hotfix 流程

### 1. 建立 hotfix branch
```bash
git checkout -b hotfix/描述
```

### 2. 修改 version.txt
```
1.3.8-hotfix.1
```

### 3. 修改 main.py
```python
__version__ = "1.3.8-hotfix.1"
```

### 4. Push 同 merge
```bash
git add -A
git commit -m "hotfix: 描述問題"
git push origin hotfix/描述
# 然後 merge 到 main
git checkout main
git merge hotfix/描述
git push origin main
```

### 5. Admin Panel 更新
`/admin` → 更新 → 「立即更新」

## 最近 Hotfix 記錄

| 版本 | 問題 | 修復 |
|------|------|------|
| v1.3.5 | JS syntax error (literal newline) | aiStudyPlan 字串修復 |
| v1.3.2 | Flask 啟動 crash | 移除重複 ai_ask route |
| v1.3.4 | 更新系統 500 | GH_RAW 未定義 |
