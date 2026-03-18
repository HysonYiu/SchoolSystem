# API 参考

完整的 SchoolSystem REST API 文档。

**基础 URL:** `http://your-device-ip:8081`
**认证:** Cookie 认证 (30 天有效期)
**内容类型:** `application/json`

---

## 认证

### 获取认证 Cookie

首次访问时需要输入 `SECRET_KEY`：

```
POST /login
Content-Type: application/x-www-form-urlencoded

key=your-secret-key
```

**响应:**
```json
{
  "status": "success"
}
```

Cookie 设置后，后续请求自动使用。

---

## 今日功课

### 获取今日功课 + Cycle Day

```
GET /api/today
```

**响应:**
```json
{
  "date": "2025-03-18",
  "cycle_day": 3,
  "cycle_day_name": "Wednesday",
  "homework": [
    {
      "id": 1,
      "title": "English Essay",
      "subject": "ENG",
      "hw_type": "功課",
      "due_date": "2025-03-20",
      "priority": "高",
      "done": false,
      "days_left": 2
    }
  ],
  "exams": [
    {
      "id": 5,
      "title": "Math Final",
      "exam_date": "2025-04-15",
      "countdown": 28
    }
  ]
}
```

---

## 功课管理

### 获取功课列表

```
GET /api/hw?done=0&subject=ENG&limit=50
```

**查询参数:**
- `done` (0|1): 筛选完成状态 (默认: 不筛选)
- `subject` (string): 筛选科目 (默认: 所有)
- `limit` (number): 返回数量 (默认: 50)

**响应:**
```json
{
  "total": 15,
  "done": 8,
  "pending": 7,
  "completion_rate": "53%",
  "homework": [
    {
      "id": 1,
      "title": "Physics Lab Report",
      "subject": "CHEM",
      "hw_type": "報告",
      "due_date": "2025-03-22",
      "priority": "中",
      "done": false,
      "created_at": "2025-03-18T10:30:00",
      "updated_at": "2025-03-18T10:30:00"
    }
  ],
  "stats": {
    "by_subject": {
      "ENG": 5,
      "CHI": 3,
      "MATH": 4
    },
    "by_type": {
      "功課": 8,
      "小測": 2,
      "報告": 5
    }
  }
}
```

### 新增功课

```
POST /api/hw
Content-Type: application/json

{
  "title": "Chemistry Assignment",
  "subject": "CHEM",
  "hw_type": "功課",
  "due_date": "2025-03-25",
  "priority": "高"
}
```

**必需字段:** `title`, `subject`, `hw_type`, `due_date`
**可选字段:** `priority` (默认: "中")

**响应:**
```json
{
  "id": 42,
  "status": "success",
  "message": "功课已新增"
}
```

### 标记功课完成

```
POST /api/hw/42/done
```

**响应:**
```json
{
  "status": "success",
  "message": "已标记为完成"
}
```

### 撤销完成状态

```
POST /api/hw/42/undone
```

**响应:**
```json
{
  "status": "success",
  "message": "已撤销完成状态"
}
```

### 删除功课

```
DELETE /api/hw/42
```

**响应:**
```json
{
  "status": "success",
  "message": "功课已删除"
}
```

---

## 课程表

### 获取 Cycle Day 信息

```
GET /api/cycle
```

**响应:**
```json
{
  "cycle_day": 3,
  "day_name": "Wednesday",
  "cycle_start": "2025-09-02",
  "progress": 3,
  "remaining": 4
}
```

### 获取课程表

```
GET /api/timetable?day=3
```

**查询参数:**
- `day` (1-7): Cycle Day 编号 (默认: 当前)

**响应:**
```json
{
  "day": 3,
  "classes": [
    {
      "time": "08:20-09:00",
      "subject": "ENG",
      "room": "Rm42"
    },
    {
      "time": "09:00-09:40",
      "subject": "MATH",
      "room": "Rm51"
    }
  ]
}
```

---

## 考试管理

### 获取考试列表

```
GET /api/exams
```

**响应:**
```json
{
  "exams": [
    {
      "id": 1,
      "title": "English Language",
      "exam_date": "2025-04-10",
      "countdown": 23,
      "notes": "Paper 1 & 2"
    },
    {
      "id": 2,
      "title": "Chemistry Practical",
      "exam_date": "2025-04-15",
      "countdown": 28
    }
  ]
}
```

### 新增考试

```
POST /api/exams
Content-Type: application/json

{
  "title": "Physics Midterm",
  "exam_date": "2025-04-05",
  "notes": "Chapters 1-5"
}
```

**响应:**
```json
{
  "id": 10,
  "status": "success"
}
```

---

## 统计分析

### 获取统计信息

```
GET /api/stats
```

**响应:**
```json
{
  "stats": {
    "total": 28,
    "done": 15,
    "pending": 13,
    "completion_rate": "54%"
  },
  "by_subject": {
    "ENG": {"total": 5, "done": 3},
    "CHI": {"total": 4, "done": 2},
    "MATH": {"total": 6, "done": 4}
  },
  "by_type": {
    "功課": {"total": 18, "done": 10},
    "小測": {"total": 5, "done": 3},
    "報告": {"total": 5, "done": 2}
  },
  "overdue": [
    {
      "id": 3,
      "title": "Late Assignment",
      "days_overdue": 2
    }
  ]
}
```

---

## AI 功能

### AI 问答

```
POST /api/ai/ask
Content-Type: application/json

{
  "question": "怎樣提高記憶力讀書？"
}
```

**必需:** `question`

**响应:**
```json
{
  "answer": "提高記憶力的方法包括...（AI 回答）",
  "agent": "StudyAdvisor"
}
```

### 生成温书计划

```
POST /api/ai/study_plan
Content-Type: application/json

{
  "days": 7,
  "subjects": ["ENG", "MATH", "CHEM"]
}
```

**参数:**
- `days` (number): 规划天数 (默认: 3)
- `subjects` (array): 科目列表 (可选: 默认所有)

**响应:**
```json
{
  "plan": [
    {
      "date": "2025-03-19",
      "session": "Morning (09:00-11:00)",
      "subject": "MATH",
      "topics": ["Chapter 3", "Calculus"],
      "duration_minutes": 120,
      "free_period": false
    },
    {
      "date": "2025-03-19",
      "session": "Afternoon (14:00-16:00)",
      "subject": "ENG",
      "topics": ["Vocabulary", "Essay Writing"],
      "duration_minutes": 120,
      "free_period": false
    }
  ],
  "total_study_hours": 14,
  "recommended_breaks": 8
}
```

### 白板识别

```
POST /api/whiteboard/upload
Content-Type: multipart/form-data

file: <image-file>
subject: ENG
```

**响应:**
```json
{
  "status": "success",
  "extracted_text": "Homework: Read Chapter 5, Page 45-60...",
  "homework_added": {
    "title": "Read Chapter 5",
    "subject": "ENG",
    "hw_type": "功課",
    "due_date": "2025-03-20"
  }
}
```

---

## 录音管理

### 获取录音列表

```
GET /api/recordings?subject=ENG
```

**查询参数:**
- `subject` (string): 筛选科目

**响应:**
```json
{
  "recordings": [
    {
      "id": 1,
      "filename": "lesson_2025-03-18_1047.m4a",
      "subject": "ENG",
      "date": "2025-03-18",
      "duration": 3600,
      "url": "/api/recordings/1/download"
    }
  ]
}
```

### 上传录音

```
POST /api/recordings/upload
Content-Type: multipart/form-data

file: <audio-file>
subject: ENG
```

**支持格式:** .mp3, .m4a, .wav, .ogg, .aac, .mp4

**响应:**
```json
{
  "id": 42,
  "filename": "lesson_2025-03-18_1124.m4a",
  "subject": "ENG",
  "date": "2025-03-18",
  "duration": 2745,
  "status": "success"
}
```

### 下载录音

```
GET /api/recordings/42/download
```

---

## 管理功能

### 获取访问日志

```
GET /api/logs?n=50
```

**查询参数:**
- `n` (number): 返回记录数 (默认: 50, 最大: 1000)

**认证:** 需要管理员密钥

**响应:**
```json
{
  "logs": [
    {
      "id": 142,
      "ip": "192.168.1.100",
      "action": "get_homework",
      "detail": "Fetched 28 items",
      "timestamp": "2025-03-18T14:30:45"
    }
  ]
}
```

### 检查更新

```
GET /admin/check_update
```

**认证:** 需要管理员密钥

**响应:**
```json
{
  "current_version": "2.0.0-alpha.1",
  "latest_version": "2.0.0-beta.1",
  "update_available": true,
  "changelog": "..."
}
```

### 执行更新

```
POST /admin/update
```

**认证:** 需要管理员密钥

**响应:**
```json
{
  "status": "updating",
  "message": "Update in progress, app will restart shortly"
}
```

---

## 错误处理

### 标准错误响应

```json
{
  "error": "invalid_input",
  "message": "Field 'title' is required",
  "details": {
    "field": "title"
  }
}
```

### HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 新建资源成功 |
| 400 | 无效输入 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 速率限制

目前无速率限制。生产环境建议配置。

---

## WebSocket（未来）

Discord Bot 使用 WebSocket 连接以实时接收命令。Web UI 可在将来添加 WebSocket 支持以实现实时更新。

---

## 示例 - 完整工作流

### 用户工作流示例

```bash
# 1. 获取今日功课
curl http://192.168.1.100:8081/api/today

# 2. 添加新功课
curl -X POST http://192.168.1.100:8081/api/hw \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chemistry Lab",
    "subject": "CHEM",
    "hw_type": "實驗",
    "due_date": "2025-03-22",
    "priority": "高"
  }'

# 3. 查看所有功课
curl http://192.168.1.100:8081/api/hw?done=0

# 4. 标记功课完成
curl -X POST http://192.168.1.100:8081/api/hw/42/done

# 5. 获取统计信息
curl http://192.168.1.100:8081/api/stats

# 6. 请求 AI 温书计划
curl -X POST http://192.168.1.100:8081/api/ai/study_plan \
  -H "Content-Type: application/json" \
  -d '{"days": 7}'
```

