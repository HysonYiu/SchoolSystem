# 貢獻指南

感謝你對 SchoolSystem 的興趣！本指南將幫助你理解如何為這個項目貢獻代碼。

## 行為準則

請閱讀並遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。我們承諾建立一個包容、尊重的社區。

## 快速開始

### 開發環境設置

#### 1. Clone 代碼庫

```bash
git clone https://github.com/SchoolSystemYiu/SchoolSystem.git
cd SchoolSystem
```

#### 2. 創建虛擬環境

```bash
# 使用 venv（Python 3.10+）
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### 3. 安裝依賴

```bash
# 安裝生產環境依賴
pip install -r requirements.txt

# 安裝開發工具依賴
pip install -r requirements-dev.txt

# 安裝 pre-commit hooks
pre-commit install
```

#### 4. 驗證設置

```bash
# 運行代碼風格檢查
black --check .
flake8 .
isort --check .

# 運行測試
pytest tests/
```

## 開發工作流

### 創建新的 Feature 分支

```bash
git checkout -b feature/your-feature-name
```

**分支命名約定：**
- 新功能：`feature/descriptive-name`
- Bug 修復：`bugfix/issue-description`
- 文檔：`docs/description`
- 快速修復：`hotfix/description`

### 代碼風格

#### Python 風格指南

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)，並使用工具自動化檢查：

**代碼格式化：**
```bash
black --line-length=100 .
```

**導入排序：**
```bash
isort --profile=black --line-length=100 .
```

**靜態檢查：**
```bash
flake8 . --max-line-length=100 --extend-ignore=E203
```

#### Python 編碼標準

- 函數和變量：`snake_case`
- 類：`PascalCase`
- 常數：`UPPER_SNAKE_CASE`
- 私有方法/變量：`_leading_underscore`

#### Docstrings

使用 Google 風格 docstrings：

```python
def get_homework(user_id: int, done: bool = False) -> list[dict]:
    """
    獲取用戶的功課列表。

    Args:
        user_id: 用戶 ID
        done: 是否只獲取已完成的功課，默認為 False

    Returns:
        功課字典列表

    Raises:
        ValueError: 如果 user_id 無效
    """
    pass
```

### 提交 Pull Request

#### PR 檢查清單

提交前，請確保：

- [ ] 分支基於最新的 `main`
- [ ] 本地代碼風格檢查通過：`black --check .` + `flake8 .` + `isort --check .`
- [ ] 新增代碼有相應測試
- [ ] 所有現有測試通過：`pytest tests/`
- [ ] 代碼覆蓋率 ≥ 70%（如適用）
- [ ] 更新相關文檔（README.md, CHANGELOG.md 等）

#### PR 模板

```markdown
## 概述
簡要說明此 PR 的目的

## 相關 Issue
Fixes #123（如果適用）

## 變更類型
- [ ] Bug 修復
- [ ] 新功能
- [ ] 文檔更新
- [ ] 性能優化
- [ ] 重構

## 詳細描述
詳細解釋變更內容和原因

## 測試
描述你測試過的情況

## 截圖（如適用）
```

### 自動檢查

提交後，GitHub Actions 將自動運行：

1. **Linting** - 代碼風格檢查
2. **Testing** - 單元測試和覆蓋率
3. **Release** - 版本管理（標籤推送時）

所有檢查必須通過才能合併。

## 報告 Bug

### Bug 報告模板

使用此模板提交 GitHub Issue：

```markdown
## 描述
清楚簡潔的 bug 描述

## 重現步驟
1. 第一步
2. 第二步
3. 觀察問題

## 預期行為
應該發生什麼

## 實際行為
實際發生什麼

## 環境
- OS: [e.g., Windows, macOS, Linux]
- Python 版本: [e.g., 3.10, 3.11]
- SchoolSystem 版本: [e.g., v2.0.0-alpha.1]

## 日誌
```
粘貼相關日誌或錯誤信息
```
```

## 提功能建議

使用 GitHub Discussions 或 Issue（標籤 `enhancement`）提出建議。

## 提交信息約定

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 風格：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型：**
- `feat` - 新功能
- `fix` - Bug 修復
- `docs` - 文檔
- `style` - 代碼風格（import 排序、格式化等）
- `refactor` - 代碼重構
- `perf` - 性能優化
- `test` - 測試相關
- `chore` - 構建、依賴、工具等

**示例：**
```
feat(homework): add homework completion status tracking

- Add `completed_at` timestamp field
- Add completion status in API response
- Update tests

Closes #42
```

## 版本管理

### 版本方案

遵循 [Semantic Versioning](https://semver.org/)：

- **MAJOR.MINOR.PATCH**
  - MAJOR：不兼容 API 變更
  - MINOR：向後相容新功能
  - PATCH：向後相容 bug 修復

- **Pre-release 版本**：`v2.0.0-alpha.1`, `v2.0.0-beta.1`

### 發布流程

1. 更新 `version.txt` 和 `pyproject.toml`
2. 更新 `CHANGELOG.md`
3. 創建 git tag：`git tag v2.0.0`
4. 推送標籤：`git push origin v2.0.0`
5. GitHub Actions 自動生成 Release

## 問題或需要幫助？

- 📖 閱讀 [文檔](docs/)
- 🐛 查看 [已知問題](TODO.md)
- 💬 在 Discussions 中提問
- 📧 聯繫維護者

## 許可

通過貢獻代碼，你同意你的代碼將遵循 MIT License 發布。

---

感謝貢獻！🎉

