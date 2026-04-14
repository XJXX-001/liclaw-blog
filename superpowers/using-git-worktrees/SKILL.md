---
name: using-git-worktrees
description: 当需要在隔离环境中开发时使用 — 使用 Git Worktree 避免分支切换。
---

# Using Git Worktrees

## 为什么用 Worktree

**问题：** 在主分支上开发危险，频繁切换分支麻烦。

**解决：** Git Worktree 在独立目录创建工作副本，同时在多个分支工作。

## 核心概念

```
仓库
├── main                    # 主分支
├── worktree-feature-1      # 功能 1 的工作树
├── worktree-feature-2      # 功能 2 的工作树
└── worktree-bugfix        # Bugfix 的工作树
```

每个 worktree 是独立的目录，可以同时在不同分支工作。

## 命令

### 查看现有 worktrees

```bash
git worktree list
```

### 创建新 worktree

```bash
git worktree add ../worktree-feature-x -b feature-x
```

解释：
- `../worktree-feature-x` — 新工作树的目录位置
- `-b feature-x` — 创建并切换到新分支

### 移除 worktree

```bash
git worktree remove ../worktree-feature-x
```

## 使用场景

### 场景 1：隔离功能开发

```
正在 main 上 hotfix
    ↓
需要同时开发新功能
    ↓
创建 worktree
git worktree add ../worktree-new-feature -b new-feature
    ↓
在 worktree 里开发新功能
同时 main 上的 hotfix 继续
```

### 场景 2：隔离审查

```
收到代码审查请求
    ↓
创建 worktree 检入审查代码
git worktree add ../worktree-review -b review-branch
    ↓
在隔离环境审查代码
    ↓
审查完成后删除 worktree
git worktree remove ../worktree-review
```

### 场景 3：保持工作进度

```
在 feature 分支工作到一半
    ↓
需要紧急在 main 修复
    ↓
main 创建 worktree
git worktree add ../worktree-hotfix -b hotfix
    ↓
在 hotfix worktree 修复
    ↓
完成后切回 feature worktree
```

## OpenClaw 中的工作流

### 创建 Worktree

```bash
# 派生任务：创建 worktree
git fetch origin
git worktree add ../worktree-task-name -b task/description
cd ../worktree-task-name
```

### 在 Worktree 中工作

```bash
cd ../worktree-task-name
# 正常开发、提交
git add .
git commit -m "feat: add feature"
```

### 完成后

```bash
# 推送分支
git push -u origin task/description

# 删除 worktree（如果不需要了）
git worktree remove ../worktree-task-name
```

## 最佳实践

### ✅ 推荐

- 每个 worktree 用描述性名称
- 完成后及时清理不需要的 worktree
- 先 fetch 最新 main 再创建 worktree

### ❌ 避免

- 不要在多个 worktree 同一分支工作
- 不要忽略 worktree list 中的"detached"状态
- 不要在 worktree 删除前忽略未提交的更改

## 清理

### 查看所有 worktrees

```bash
git worktree list
```

### 清理已完成的 worktree

```bash
git worktree remove ../worktree-completed-feature
```

### 清理所有 worktree（谨慎）

```bash
# 只清理已经合并到 main 的
git worktree prune
```

## 与 subagent-driven-development 整合

在开始实施计划前：

```
建议使用 worktree 隔离开发
    ↓
在 worktree 中创建分支
    ↓
在 worktree 中执行任务
    ↓
完成后推送到远程
    ↓
清理 worktree
```
