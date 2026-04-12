---
title: OpenClaw 过期 Subagent 任务残留问题排查与解决
date: 2026-04-12 18:15:00
slug: openclaw-stale-task-cleanup
tags:
  - OpenClaw
  - 问题排查
categories:
  - AI Engineering
---

## 问题现象

在飞书中与 OpenClaw 交互时，状态信息始终显示：

```
📌 Tasks: 1 active · 1 total · subagent · 完成飞书文档到静态博客的发布流程
```

但实际上这个任务早已结束（状态为 `killed`），属于过期的残留记录。

## 排查过程

### 1. 初步定位

首先使用 `subagents list` 查看任务列表：

```json
{
  "total": 1,
  "active": [],
  "recent": []
}
```

结果显示 `total=1`，但 `active` 和 `recent` 都为空，说明数据不一致。

### 2. 查找数据源

OpenClaw 的任务数据存储在多个位置：

1. **`~/.openclaw/subagents/runs.json`** - 子代理运行记录（JSON 格式）
2. **`~/.openclaw/tasks/runs.sqlite`** - 任务运行记录（SQLite 数据库）
3. **`~/.openclaw/flows/registry.sqlite`** - 流程注册表（SQLite 数据库）

### 3. 数据清理

#### 清理 `runs.json`

查看文件内容：

```json
{
  "version": 2,
  "runs": {
    "2ab69921-3e7a-42f1-b83a-32f6e54e7731": {
      "outcome": {"status": "error", "error": "killed"},
      "endedReason": "subagent-killed"
    }
  }
}
```

任务已标记为 `killed`，但记录未清理。直接清空 `runs` 对象：

```json
{
  "version": 2,
  "runs": {}
}
```

#### 清理 `tasks/runs.sqlite`

使用 Python 查询数据库：

```python
import sqlite3
conn = sqlite3.connect('~/.openclaw/tasks/runs.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM task_runs WHERE source_id='...'")
# 发现 2 条记录，status='running' 但实际已结束
cursor.execute("DELETE FROM task_runs WHERE source_id='...'")
conn.commit()
```

#### 清理 `flows/registry.sqlite`

```python
conn = sqlite3.connect('~/.openclaw/flows/registry.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM flow_runs")
# 发现 1 条记录，status='running'
cursor.execute("DELETE FROM flow_runs")
conn.commit()
```

### 4. 重启 Gateway

清理数据库后，需要重启 Gateway 以刷新内存缓存：

```bash
openclaw gateway restart
```

重启后验证：

```json
{
  "total": 0,
  "active": [],
  "recent": []
}
```

问题解决。

## 问题分析

### 根因

OpenClaw 的 subagent 任务在异常结束（如被 `killed`）时，任务记录未能正确清理：

1. **状态不一致**：任务在 `runs.json` 中标记为 `killed`，但在 SQLite 数据库中仍为 `running`
2. **多数据源**：任务记录分散在三个数据源，清理时需全部处理
3. **缓存机制**：Gateway 启动时加载任务计数器到内存，数据库清理后需重启才能刷新

### 影响范围

- 状态显示不准确（显示过期任务为 active）
- 对功能无实际影响（过期任务不会被执行）

## 解决方案总结

```bash
# 1. 清理 runs.json
echo '{"version":2,"runs":{}}' > ~/.openclaw/subagents/runs.json

# 2. 清理 SQLite 数据库（需根据实际情况筛选）
python3 -c "
import sqlite3
# 清理 tasks 数据库
conn = sqlite3.connect('~/.openclaw/tasks/runs.sqlite')
conn.execute(\"DELETE FROM task_runs WHERE status='running' AND source_id='<过期任务ID>'\")
conn.commit()
conn.close()
# 清理 flows 数据库
conn = sqlite3.connect('~/.openclaw/flows/registry.sqlite')
conn.execute(\"DELETE FROM flow_runs WHERE status='running'\")
conn.commit()
conn.close()
"

# 3. 重启 Gateway
openclaw gateway restart
```

## 经验总结

1. **多数据源问题**：OpenClaw 的任务数据分散存储，排查时需全面检查
2. **状态同步**：异常终止的任务可能导致状态不一致
3. **缓存清理**：数据库修改后需要重启服务才能生效

## 建议

这是一个小的 Bug，建议 OpenClaw 团队：
- 在 subagent 异常结束时自动清理残留记录
- 或定期扫描并清理状态不一致的任务记录
- 统一数据源，避免多源同步问题

---

*问题已解决，过期任务彻底清除。*
