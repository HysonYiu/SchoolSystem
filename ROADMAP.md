# 🗺️ SchoolSystem Project Roadmap

> Kanban-style project board with Milestones, Priorities, and Status tracking

**Last Updated:** 2026-03-18
**Current Version:** v2.0.0-alpha.1
**Active Milestone:** v2.0.0-beta

---

## 📊 Project Overview

```
Legend:
🟢 Done       | 🟡 In Progress | 🔵 In Review | ⚪ Backlog | 🔴 Blocked
P0 = Critical | P1 = High      | P2 = Medium  | P3 = Low
S = Small     | M = Medium     | L = Large    | XL = Extra Large
```

---

## 🚀 v2.0.0-beta (Target: May 31, 2025)

**Focus:** Discord Bot Enhancement, AI Agent Improvements, Stability

### 🟢 Completed
- [x] Project standardization (dependencies, CI/CD, docs)
- [x] README modernization
- [x] Type hints guide + docstrings specification
- [x] Testing framework setup (pytest)

### 🟡 In Progress
- [ ] [#15] Discord Bot pagination for `/hw` (P1, M)
- [ ] [#16] AI Agent system enhancement (P1, L)
- [ ] [#17] Study plan PDF export (P2, M)

### 🔵 In Review
- [ ] [#12] Fix event loop conflict on bot startup (P0, S)
- [ ] [#13] Improve whiteboard recognition accuracy (P1, M)

### ⚪ Backlog
- [ ] [#18] Auto-reconnect for Discord Bot (P2, M)
- [ ] [#19] Improve daily reminder messages with Embed charts (P2, M)
- [ ] [#20] Add DM reminders for exam deadlines (P2, M)
- [ ] [#21] Add due date autocomplete for `/add` command (P3, M)
- [ ] [#22] Display homework list in `/done` command (P3, S)
- [ ] [#23] HomeworkAgent implementation (P1, L)
- [ ] [#24] StudyAgent dynamic adjustment (P1, L)
- [ ] [#25] TimetableAgent free period detection (P1, M)
- [ ] [#26] Study plan history tracking (P2, M)
- [ ] [#27] Dynamic study plan adjustment (P2, M)

### 🔴 Known Issues
- [ ] Discord Bot first startup may have event loop conflicts (P0)
- [ ] Whiteboard recognition needs DeepSeek Vision model (P1)
- [ ] Cycle Day calculation may be inaccurate during exam periods (P2)

---

## 📈 v2.1.0 (Target: July 31, 2025)

**Focus:** Statistics, Tracking, and Analytics

### Features

#### Statistics Dashboard Enhancement
- [ ] [#30] Score tracking (test/exam records) (P1, L)
- [ ] [#31] Study hours tracker with timer (P2, M)
- [ ] [#32] Weekly learning reports (P1, M)
- [ ] [#33] Subject completion rate charts (P2, M)

#### Chemistry PDF Auto-parsing
- [ ] [#34] Google Classroom PDF download (P2, M)
- [ ] [#35] DeepSeek Vision chemistry homework parsing (P1, L)
- [ ] [#36] Auto-add homework (skip completed ones) (P1, M)
- [ ] [#37] Strikethrough detection for completed items (P2, S)

#### Data Export
- [ ] [#38] Export study plan as PDF (P1, M)
- [ ] [#39] Export homework list as CSV/JSON (P2, M)
- [ ] [#40] Export statistics report (P2, M)

### Backlog
- [ ] API endpoint optimization (P2, M)
- [ ] Database query optimization (P2, L)
- [ ] Caching layer implementation (P3, L)

---

## 🌟 v2.2.0 (Target: September 30, 2025)

**Focus:** Multi-User, Notifications, and Platform Expansion

### Multi-User Support
- [ ] [#50] User authentication system (P1, L)
- [ ] [#51] User profile management (P1, M)
- [ ] [#52] Shared timetables and homework (P2, L)
- [ ] [#53] Permission system (admin, member, guest) (P2, M)

### Push Notifications
- [ ] [#60] Push notification service (P1, L)
- [ ] [#61] Homework deadline alerts (P1, M)
- [ ] [#62] Exam countdown notifications (P1, M)
- [ ] [#63] Study reminder notifications (P2, M)

### Platform Expansion
- [ ] [#70] iOS widget support (P2, L)
- [ ] [#71] Siri Shortcuts integration (P2, M)
- [ ] [#72] Apple Watch app (P3, L)
- [ ] [#73] Database export/import (P2, M)

### Backlog
- [ ] Web app PWA conversion (P3, M)
- [ ] Android native app (P3, L)

---

## 🎯 v2.3.0 (Target: December 31, 2025)

**Focus:** Future Enhancements and Long-term Features

### Advanced Features
- [ ] [#80] Collaborative study groups (P3, L)
- [ ] [#81] AI tutoring chatbot (P3, L)
- [ ] [#82] Grade prediction system (P3, L)
- [ ] [#83] Adaptive study recommendations (P3, L)

### Performance & Infrastructure
- [ ] [#90] Microservices architecture (P3, L)
- [ ] [#91] Database replication/backup (P3, M)
- [ ] [#92] Kubernetes deployment (P3, L)
- [ ] [#93] API rate limiting (P3, M)

### Community
- [ ] [#100] Community homework library (P3, L)
- [ ] [#101] Study group matching (P3, L)
- [ ] [#102] Resources marketplace (P3, L)

---

## ✅ Completed Features

### v1.0.0 (Dec 2024)
- [x] Basic homework CRUD operations
- [x] Exam countdown management
- [x] SQLite database setup
- [x] Basic authentication (SECRET_KEY)

### v1.1.0 (Jan 2025)
- [x] Cycle Day calculation (7-day system)
- [x] Timetable management (Day 1-7)
- [x] Basic AI assistant
- [x] Admin panel foundation

### v1.2.0 (Jan 2025)
- [x] Audio recording feature
- [x] Undo functionality for completed homework
- [x] Admin update system

### v1.3.0-1.3.8 (Feb 2025)
- [x] Discord Bot with Slash Commands
- [x] Whiteboard photo upload + AI recognition
- [x] Admin panel redesign
- [x] Git pull update system
- [x] Watchdog auto-restart mechanism
- [x] Daily reminder notifications

### v2.0.0-alpha (Mar 2025)
- [x] AI study plan generation (exams + free periods + holidays)
- [x] Today's priority items (no AI key required)
- [x] Project standardization (Tier 1-3)
- [x] Comprehensive documentation
- [x] Testing framework setup
- [x] Type hints guide

---

## 🎪 Milestone Status

| Milestone | Target Date | Progress | Status |
|-----------|------------|----------|--------|
| **v2.0.0-beta** | May 31, 2025 | 40% | 🟡 On Track |
| **v2.1.0** | Jul 31, 2025 | 0% | ⚪ Planned |
| **v2.2.0** | Sep 30, 2025 | 0% | ⚪ Planned |
| **v2.3.0** | Dec 31, 2025 | 0% | ⚪ Planned |

---

## 📋 How to Use This Roadmap

### For Users
- View the roadmap to understand upcoming features
- Check milestone status for expected delivery dates
- Leave feedback on features you'd like to see

### For Contributors
- Pick a task from **Backlog** and assign it to yourself
- Move tasks through the board: Backlog → In Progress → Review → Done
- Link your PR to the related issue
- Update task status regularly

### For Maintainers
1. Update milestone status monthly
2. Move completed items to Done
3. Adjust priorities based on feedback
4. Release notes reference this roadmap

---

## 🔄 Status Flow

```
⚪ Backlog
    ↓ (Pick up)
🟡 In Progress
    ↓ (Ready for review)
🔵 In Review (PR opened)
    ↓ (Approved & merged)
🟢 Done
```

---

## 📞 Feedback & Suggestions

Have ideas for new features? Found a bug? Want to help?

- 💬 [GitHub Discussions](https://github.com/SchoolSystemYiu/SchoolSystem/discussions) - Feature requests & ideas
- 🐛 [GitHub Issues](https://github.com/SchoolSystemYiu/SchoolSystem/issues) - Bug reports
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute

---

## 📈 Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Test Coverage | 30% | 70%+ |
| Documentation | 90% | 100% |
| Type Hints | 20% | 80%+ |
| Code Quality (Flake8) | ✅ Pass | ✅ Pass |

---

<div align="center">

**Last Updated:** 2026-03-18
**Maintained by:** [@SchoolSystemYiu](https://github.com/SchoolSystemYiu)
**See Also:** [CHANGELOG.md](CHANGELOG.md) | [TODO.md](TODO.md) | [Contributing Guide](CONTRIBUTING.md)

</div>
