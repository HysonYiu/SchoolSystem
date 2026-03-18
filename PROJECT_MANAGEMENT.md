# 📊 Project Management Guide

Complete guide to managing SchoolSystem project using GitHub Milestones, Issues, and Project Board.

---

## 📋 Overview

```
ROADMAP.md (Project Vision)
    ↓
GitHub Milestones (Version Planning)
    ↓
GitHub Project Board (Kanban Board)
    ↓
GitHub Issues (Individual Tasks)
    ↓
Pull Requests (Implementation)
```

---

## 🎯 Milestones

### Purpose
Track feature development across major versions and timelines.

### Current Milestones

| Milestone | Due Date | Focus |
|-----------|----------|-------|
| **v2.0.0-beta** | May 31, 2025 | Discord Bot, AI Agent |
| **v2.1.0** | Jul 31, 2025 | Statistics, PDF Export |
| **v2.2.0** | Sep 30, 2025 | Multi-user, Notifications |
| **v2.3.0** | Dec 31, 2025 | Future Features |

### How to Manage Milestones

1. **Create New Milestone** (Maintainers only)
   ```bash
   gh milestone create "v2.1.0" \
     --description "Statistics and analytics" \
     --due-date 2025-07-31
   ```

2. **Associate Issues to Milestone**
   - Open issue details
   - Set milestone in right sidebar
   - Issues automatically appear in ROADMAP.md

3. **Track Progress**
   - View milestone page: `/projects/SchoolSystem/milestones`
   - Monitor: % complete, due date, open/closed issues

4. **Close Milestone** (When released)
   - All issues must be closed or moved
   - Close milestone after release
   - Create release notes

---

## 🗂️ Issue Tracking

### Issue Labels

**Type:**
- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Docs need update
- `task` - Internal task/subtask
- `question` - Question/discussion

**Priority:**
- `P0` - Critical (security, data loss, major crash)
- `P1` - High (major feature, significant bug)
- `P2` - Medium (normal work)
- `P3` - Low (nice-to-have, polish)

**Status:**
- `backlog` - Not yet started
- `in-progress` - Actively being worked on
- `in-review` - PR submitted, waiting review
- `done` - Completed and merged

**Component:**
- `web-ui` - Web interface
- `discord-bot` - Discord integration
- `api` - Backend/REST API
- `database` - Data storage
- `ai-agent` - AI features
- `testing` - Tests, CI/CD
- `docs` - Documentation

### Creating Issues

#### Bug Reports
1. Use `.github/ISSUE_TEMPLATE/bug_report.md` template
2. Provide clear reproduction steps
3. Include system information
4. Add `bug` label and priority
5. Assign to component

#### Feature Requests
1. Use `.github/ISSUE_TEMPLATE/feature_request.md` template
2. Describe use case clearly
3. Suggest solution and alternatives
4. Add `enhancement` label and priority
5. Link to ROADMAP.md if applicable

#### Tasks
1. Use `.github/ISSUE_TEMPLATE/task.md` template
2. Break into subtasks
3. Set acceptance criteria
4. Add `task` label and priority
5. Assign to team member

---

## 📊 GitHub Project Board

### Purpose
Visual Kanban board for tracking work-in-progress.

### Columns

| Column | Status | When to Use |
|--------|--------|-----------|
| 📋 **Backlog** | Not started | Issue just created or prioritized |
| 🟡 **In Progress** | Active work | Developer assigned and working |
| 🔵 **In Review** | Awaiting merge | PR submitted, under review |
| ✅ **Done** | Complete | PR merged, issue closed |

### Workflow

```
1. Create Issue (Backlog)
   ↓
2. Assign to Developer (Still in Backlog)
   ↓
3. Developer starts work (Move to In Progress)
   ↓
4. Developer opens PR (Move to In Review)
   ↓
5. PR approved & merged (Auto-move to Done)
   ↓
6. Issue auto-closes (Done - archived)
```

### How to Use

1. **Add Cards to Board**
   - Issues automatically appear in "Backlog" column
   - Click "Add cards" if not visible

2. **Move Cards**
   - Drag between columns as status changes
   - Card moves automatically when PR is opened
   - Card auto-closes when issue closes

3. **Organize Within Column**
   - Drag to prioritize
   - Top = higher priority

4. **View & Filter**
   - Filter by label, assignee, milestone
   - Save custom views

---

## 👥 Team Roles & Permissions

### Contributor (Everyone)
- ✅ Can: Create issues, comment, open PRs
- ❌ Cannot: Close/edit others' issues, merge PRs, create milestones

### Maintainer (Repository Owner)
- ✅ Can: All contributor rights + approve PRs, close issues, manage milestones
- ✅ Should: Review, maintain roadmap, release versions

### Admin (Repository Owner)
- ✅ Can: Everything including repository settings, delete content

---

## 🔄 Workflow Example

### Reporting a Bug

```
1. User finds bug
2. Opens GitHub issue with bug_report template
3. Includes: reproduction steps, screenshots, environment info
4. Maintainer reviews and labels with:
   - `bug` label
   - `P1` or `P2` priority
   - Component label
   - Milestone (if for specific version)
5. Issue appears in project board "Backlog"
6. Developer picks up and moves to "In Progress"
7. Developer opens PR, issue moves to "In Review"
8. PR gets approved and merged
9. Issue auto-closes, card moves to "Done"
```

### Implementing a Feature

```
1. Feature discussed in roadmap or GitHub Discussions
2. Create issue with feature_request template
3. Include: use case, proposed solution, alternatives
4. Maintainer labels:
   - `enhancement` label
   - `P1` or `P2` priority
   - Component label
   - `v2.x.x` milestone
5. Add to project board
6. Developer assigns and moves to "In Progress"
7. Creates feature branch: `feature/xyz`
8. Opens PR with full checklist
9. Handles code review feedback
10. PR merged → issue closed → card done
```

---

## 📈 Tracking Progress

### Dashboard View

**Every month, check:**

1. **Milestone Progress**
   - Open: `https://github.com/SchoolSystemYiu/SchoolSystem/milestones`
   - Check % complete for current milestone
   - Adjust due date if needed

2. **Project Board Health**
   - Open: `https://github.com/SchoolSystemYiu/SchoolSystem/projects`
   - Ensure In Progress items have assignees
   - Look for blocked items

3. **Open Issues**
   - Filter by milestone and priority
   - Ensure P0 issues are being addressed
   - Close old/stale issues

### Metrics to Track

| Metric | Target | Check |
|--------|--------|-------|
| Avg PR review time | < 48h | Weekly |
| Milestone completion | On time | Monthly |
| Issue response time | < 24h | Weekly |
| Test coverage | 70%+ | Per PR |
| Open vs closed issues | Trending down | Monthly |

---

## 🚀 Release Process

### Before Release

1. **Freeze Features**
   - Close milestone for new issues
   - Move incomplete items to next milestone

2. **Quality Check**
   - Run full test suite
   - Check test coverage (aim for 70%+)
   - Review all merged PRs

3. **Update Documentation**
   - Update CHANGELOG.md
   - Update version in all files
   - Update ROADMAP.md

4. **Testing**
   - QA testing in staging
   - User acceptance testing
   - Security review

### Release

1. **Create Release Tag**
   ```bash
   git tag -a v2.0.0 -m "Release v2.0.0"
   git push origin v2.0.0
   ```

2. **GitHub Release**
   - GitHub Actions auto-creates release draft
   - Edit with release notes from CHANGELOG.md
   - Publish release

3. **Announce**
   - Post to Discord
   - Update social media
   - Notify users

4. **Close Milestone**
   - Close GitHub milestone
   - Celebrate! 🎉

---

## 🐛 Issue Triage

### Process (Weekly)

1. **Review new issues**
   - Add labels if missing
   - Ask for clarification if needed
   - Duplicate check

2. **Prioritize**
   - P0: Security/critical bugs - assign immediately
   - P1: Important features/bugs - assign this week
   - P2: Normal work - add to backlog
   - P3: Nice-to-have - add to roadmap only

3. **Assign to Milestone**
   - If for current version: assign now
   - If for future version: add to roadmap only
   - If blocked: label as blocked, explain

4. **Move to Project Board**
   - Backlog column
   - Ready for developers to pick up

---

## 💡 Best Practices

### For Contributors
- ✅ Link your PR to related issues
- ✅ Keep PRs focused (one feature/fix per PR)
- ✅ Reference issue in commit message: `Fix #42`
- ✅ Update your issue status regularly
- ❌ Don't close others' issues
- ❌ Don't assign to maintainers without asking

### For Maintainers
- ✅ Review PRs within 48 hours
- ✅ Keep milestones up-to-date
- ✅ Triage new issues weekly
- ✅ Update ROADMAP.md monthly
- ✅ Close stale issues (> 30 days inactive)
- ❌ Don't create issues for your own work (update existing)
- ❌ Don't merge your own PRs without review

### For Everyone
- ✅ Use issue templates
- ✅ Search for duplicates before creating
- ✅ Use labels consistently
- ✅ Keep discussion on-topic
- ✅ Be respectful and constructive
- ❌ Don't spam or self-promote

---

## 🔗 Related Documentation

- [Roadmap](ROADMAP.md) - Project vision and features
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Release history
- [TODO.md](TODO.md) - Legacy todo list

---

## 📞 Support

Questions about project management?
- 💬 [GitHub Discussions](https://github.com/SchoolSystemYiu/SchoolSystem/discussions)
- 📧 Contact maintainer
- 📖 Read this guide again

---

**Last Updated:** 2026-03-18
**Maintained by:** [@SchoolSystemYiu](https://github.com/SchoolSystemYiu)

