# 类型提示 & Docstrings 指南

本指南说明如何为 SchoolSystem 项目添加类型提示和 Google 风格 docstrings。

## 概述

Python 类型提示帮助：
- 改进代码可读性
- 启用 IDE 自动补完
- 检测潜在的类型错误
- 生成更好的文档

## 项目范围

应在以下模块添加类型提示（优先级从高到低）：

1. **main.py** - 所有路由处理函数和数据库操作
2. **agent.py** - 所有代理类和处理函数
3. **bot.py** - Discord 命令处理函数
4. **study_plan.py** - 温书计划生成函数
5. **timetable.py** - 时间表数据和查询函数
6. **recording.py** - 录音处理函数
7. **ui.py** - 可选（大多是 HTML 字符串）

---

## 类型提示规范

### 1. 基本类型

```python
# ❌ 无类型
def get_homework():
    pass

# ✅ 有类型
def get_homework() -> list[dict[str, Any]]:
    pass

# ✅ 带参数类型
def add_homework(title: str, subject: str, due_date: str) -> int:
    pass

# ✅ 可选参数
def get_homework(
    done: bool | None = None,
    subject: str | None = None
) -> list[dict[str, Any]]:
    pass
```

### 2. 常见类型

```python
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import date, datetime

# 基本类型
def func(
    name: str,
    age: int,
    score: float,
    active: bool
) -> None:
    pass

# 容器类型
def get_items() -> list[str]:  # Python 3.9+
    pass

def get_mapping() -> dict[str, int]:  # Python 3.9+
    pass

# 元组
def get_coords() -> tuple[float, float, float]:
    pass

# Union 类型
def parse_value(value: str | int) -> float:
    pass

# Optional（等同于 Union[T, None]）
def get_optional(key: str) -> str | None:
    pass

# 日期类型
def add_homework(due_date: str | date) -> int:
    pass

# 字典和列表组合
def get_homework_dict() -> dict[str, Any]:
    """Return homework with mixed value types"""
    pass

def get_homework_list() -> list[dict[str, Any]]:
    """Return list of homework dictionaries"""
    pass
```

### 3. 数据库相关

```python
import sqlite3

def get_db() -> sqlite3.Connection:
    """Get database connection"""
    pass

def query_homework(done: bool) -> list[sqlite3.Row]:
    """Query homework from database"""
    pass

def insert_homework(
    title: str,
    subject: str,
    hw_type: str,
    due_date: str,
    priority: str = '中'
) -> int:
    """Insert homework and return ID"""
    pass
```

### 4. Flask 相关

```python
from flask import Request, Response
from werkzeug.datastructures import Headers

def handle_request(request: Request) -> Response | tuple[dict, int]:
    """Handle Flask request and return response"""
    pass

def auth(request: Request) -> bool:
    """Check if request is authenticated"""
    pass

def log_action(
    request: Request,
    action: str,
    detail: str
) -> None:
    """Log user action"""
    pass
```

### 5. Discord.py 相关

```python
import discord
from discord import app_commands

@tree.command(name="example", description="Example command")
async def example_command(interaction: discord.Interaction) -> None:
    """Handle Discord slash command"""
    await interaction.response.send_message("Response")

async def send_embed(
    channel: discord.TextChannel,
    title: str,
    description: str,
    color: discord.Color | int = 0x5856d6
) -> None:
    """Send Discord embed message"""
    pass
```

### 6. 复杂返回类型

```python
from typing import TypedDict

# 定义特定的 dict 类型
class HomeworkDict(TypedDict):
    id: int
    title: str
    subject: str
    hw_type: str
    done: bool
    priority: str
    due_date: str
    created_at: str
    updated_at: str

def get_homework() -> list[HomeworkDict]:
    """Get homework with typed dict"""
    pass

# 或使用 dataclass
from dataclasses import dataclass

@dataclass
class Homework:
    id: int
    title: str
    subject: str
    hw_type: str
    done: bool
    priority: str
    due_date: str
    created_at: str
    updated_at: str

def get_homework_objects() -> list[Homework]:
    """Get homework as dataclass objects"""
    pass
```

---

## Docstrings 规范

使用 **Google 风格** docstrings（PEP 257）。

### 1. 函数 Docstrings

```python
def add_homework(
    title: str,
    subject: str,
    hw_type: str,
    due_date: str,
    priority: str = '中'
) -> int:
    """
    Add new homework to database.

    Args:
        title: Homework title
        subject: Subject code (e.g., 'ENG', 'MATH')
        hw_type: Type of homework ('功課', '小測', '考試', etc.)
        due_date: Due date in ISO format (YYYY-MM-DD)
        priority: Priority level ('高', '中', '低'). Defaults to '中'.

    Returns:
        The ID of newly created homework record.

    Raises:
        ValueError: If subject or hw_type is invalid
        sqlite3.IntegrityError: If database constraint is violated

    Example:
        >>> hw_id = add_homework(
        ...     title='Chemistry Lab',
        ...     subject='CHEM',
        ...     hw_type='實驗',
        ...     due_date='2025-03-25',
        ...     priority='高'
        ... )
        >>> print(hw_id)
        42
    """
    pass
```

### 2. 类 Docstrings

```python
class SubAgent:
    """
    Base class for AI sub-agents.

    Sub-agents handle specific tasks in the agent system.
    Each agent receives user input and returns structured results.

    Attributes:
        name: Agent identifier
        model: LLM model name
        timeout: API call timeout in seconds

    Example:
        >>> agent = AddHWAgent()
        >>> result = agent.process("Add English essay due Friday")
        >>> print(result['action'])
        'add_homework'
    """

    def __init__(self, name: str, model: str = "deepseek-reasoner"):
        """
        Initialize sub-agent.

        Args:
            name: Agent identifier
            model: LLM model name. Defaults to "deepseek-reasoner".
        """
        self.name = name
        self.model = model

    def process(self, user_input: str) -> dict[str, Any]:
        """
        Process user input and return result.

        Args:
            user_input: Natural language input from user

        Returns:
            Dictionary with keys:
            - 'answer': Response text to user
            - 'action': Action to take ('add_homework', etc.)
            - 'data': Structured data for action
            - 'agent': Agent name

        Raises:
            ValueError: If input cannot be processed
            TimeoutError: If API call times out
        """
        pass
```

### 3. 模块级 Docstrings

```python
"""
main.py - SchoolSystem Flask Backend

This module implements the REST API server for SchoolSystem,
including authentication, homework management, AI integration,
and admin dashboard.

Key Components:
    - Flask app initialization and configuration
    - Route handlers for API endpoints
    - Database operations
    - Discord bot integration
    - Admin panel

Environment Variables:
    SECRET_KEY: Authentication key
    ADMIN_KEY: Admin panel access key
    DEEPSEEK_API_KEY: AI API key (optional)
    PORT: Server port (default: 8081)
"""
```

---

## 实施步骤

### main.py

```python
# 在模块顶部添加
from typing import Any, Dict, List, Optional, Union
from flask import Request, Response
import sqlite3

# 然后为关键函数添加类型提示和 docstring
@app.route("/api/hw", methods=["GET"])
def hw_list() -> Response:
    """
    Retrieve homework list.

    Returns:
        JSON response with homework data

    Raises:
        401: If not authenticated
    """
    pass

def get_db() -> sqlite3.Connection:
    """Get database connection from Flask g context."""
    pass

def auth(request: Request) -> bool:
    """Check if request has valid authentication cookie."""
    pass
```

### agent.py

```python
class OrchestratorAgent:
    """Main AI agent orchestrator."""

    def process(self, user_input: str) -> dict[str, Any]:
        """
        Process user input and route to appropriate sub-agent.

        Args:
            user_input: User's natural language input

        Returns:
            Structured result from selected sub-agent
        """
        pass

class AddHWAgent(SubAgent):
    """Agent for understanding and adding homework."""

    def process(self, user_input: str) -> dict[str, Any]:
        """
        Extract homework information from user input.

        Args:
            user_input: Description of homework to add

        Returns:
            Dictionary with extracted homework data
        """
        pass
```

### bot.py

```python
@tree.command(name="hw", description="Show all pending homework")
async def show_hw(interaction: discord.Interaction) -> None:
    """
    Display all pending homework.

    Args:
        interaction: Discord interaction object
    """
    pass

async def daily_reminder() -> None:
    """Send daily homework reminder at configured time."""
    pass
```

### study_plan.py

```python
def generate_study_plan(
    days: int = 3,
    subjects: list[str] | None = None
) -> list[dict[str, Any]]:
    """
    Generate AI-powered study plan.

    Args:
        days: Number of days to plan for. Defaults to 3.
        subjects: List of subject codes. Defaults to all subjects.

    Returns:
        List of daily study sessions with topics and timing
    """
    pass

def get_today_priorities() -> dict[str, Any]:
    """Get today's homework and exam priorities for planning."""
    pass
```

### timetable.py

```python
def get_cycle_day(ref_date: str | date | None = None) -> int:
    """
    Calculate current cycle day (1-7).

    Args:
        ref_date: Reference date. Defaults to today.

    Returns:
        Cycle day number (1-7)
    """
    pass

def is_school_day(check_date: str | date) -> bool:
    """Check if date is a school day."""
    pass

def get_timetable(day: int) -> list[tuple[str, str, str, str]]:
    """
    Get timetable for specific cycle day.

    Args:
        day: Cycle day number (1-7)

    Returns:
        List of (time, subject, room) tuples
    """
    pass
```

### recording.py

```python
@recording_bp.route("/upload", methods=["POST"])
def upload_recording() -> Response:
    """
    Handle audio file upload.

    Returns:
        JSON response with upload status
    """
    pass
```

---

## 验证类型

使用 **mypy** 进行静态类型检查：

```bash
# 安装 mypy
pip install mypy

# 检查单个文件
mypy main.py

# 检查整个项目
mypy .

# 使用配置文件（可选）
# 创建 mypy.ini 或在 pyproject.toml 中配置
```

### mypy 配置示例

```ini
# mypy.ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False  # 可选：严格模式
ignore_missing_imports = True
```

---

## 最佳实践

### 1. 渐进式迁移

不需要一次性添加所有类型提示。可以：
- 从公共 API 开始
- 逐步添加到内部函数
- 优先处理复杂函数

### 2. 类型别名

为常用类型创建别名：

```python
# 在模块顶部
HomeworkList = list[dict[str, Any]]
HomeworkDict = dict[str, Any]

# 使用
def get_homework() -> HomeworkList:
    pass
```

### 3. 处理 None

```python
# ✅ 明确表示可能为 None
def get_homework(hw_id: int) -> dict[str, Any] | None:
    pass

# ✅ 在处理结果时检查
result = get_homework(42)
if result is not None:
    print(result['title'])
```

### 4. 导入最佳实践

```python
from __future__ import annotations  # 启用延迟求值（文件顶部）

from typing import Any, Dict, List, Optional, Tuple
from datetime import date, datetime
from flask import Request, Response
import sqlite3
```

---

## 工具集成

### Pre-commit Hook

更新 `.pre-commit-config.yaml` 以包含类型检查：

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.8.0
  hooks:
    - id: mypy
      additional_dependencies: ['types-requests', 'types-PyYAML']
```

### CI/CD 集成

在 `.github/workflows/lint.yml` 中添加：

```yaml
- name: Type checking with mypy
  run: mypy . --ignore-missing-imports
```

---

## 示例：完整重构

### 之前（无类型）

```python
def hw_list():
    if not auth(request):
        return jsonify({"error":"unauthorized"}),401
    db = get_db()
    done = int(request.args.get("done","0"))
    rows = db.execute("SELECT * FROM homeworks WHERE done=?", (done,)).fetchall()
    return jsonify([dict(r) for r in rows])
```

### 之后（有类型和 docstring）

```python
def hw_list() -> Response | tuple[dict[str, str], int]:
    """
    Retrieve filtered homework list.

    Query Parameters:
        done: Filter by completion status (0=pending, 1=done)

    Returns:
        JSON array of homework objects or error response

    Raises:
        401: If request is not authenticated
    """
    if not auth(request):
        return jsonify({"error": "unauthorized"}), 401

    db: sqlite3.Connection = get_db()
    try:
        done: int = int(request.args.get("done", "0"))
    except ValueError:
        done = 0

    rows: list[sqlite3.Row] = db.execute(
        "SELECT * FROM homeworks WHERE done=?",
        (done,)
    ).fetchall()

    return jsonify([dict(row) for row in rows])
```

---

## 参考资源

- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Python Type Hints - Official Docs](https://docs.python.org/3/library/typing.html)
- [mypy - Official Documentation](http://www.mypy-lang.org/)

