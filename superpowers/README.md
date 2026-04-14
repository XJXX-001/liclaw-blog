# 🦐 OpenClaw Superpowers — Skill Index

**目录：** `workspace/skills/openclaw-superpowers/`

---

## 入口层

| Skill | 描述 |
|-------|------|
| `SOUL-SUPERPOWERS.md` | Superpowers 核心理念、规则、触发机制 |
| `brainstorming/` | 用户提出需求时使用 — 明确真正的问题 |
| `writing-plans/` | 有明确规格时使用 — 制定详细实施计划 |

---

## 执行层

| Skill | 描述 |
|-------|------|
| `subagent-driven-development/` | 执行独立任务计划时 — 子代理驱动，高质量快迭代 |
| `executing-plans/` | 顺序执行计划时 — 带检查点的顺序执行 |
| `test-driven-development/` | 实现功能时 — 红绿重构循环 |
| `dispatching-parallel-agents/` | 多个独立任务时 — 并行派发加速 |

---

## 质量层

| Skill | 描述 |
|-------|------|
| `systematic-debugging/` | 遇到 bug 时 — 系统化调试方法 |
| `verification-before-completion/` | 任务完成前 — 最终质量检查 |
| `requesting-code-review/` | 需要审查时 — 准备审查材料 |
| `receiving-code-review/` | 收到审查反馈时 — 处理和修复 |

---

## 收尾层

| Skill | 描述 |
|-------|------|
| `finishing-a-development-branch/` | 所有任务完成时 — 最终检查和合并准备 |
| `using-git-worktrees/` | 需要隔离开发时 — Git Worktree 管理 |

---

## 工具类

| Skill | 描述 |
|-------|------|
| `writing-skills/` | 创建新 Skill 时 — Skill 编写方法论 |

---

## 工作流

```
用户需求
    ↓
brainstorming（理解问题）
    ↓
writing-plans（制定计划）
    ↓
执行：
├── subagent-driven-development（推荐）
├── executing-plans（顺序）
└── dispatching-parallel-agents（并行）
    ↓
每个任务用 TDD
    ↓
verification-before-completion
    ↓
requesting/receiving-code-review
    ↓
finishing-a-development-branch
```

---

## 使用方法

在 AGENTS.md 中已配置：
- 任何任务前先检查 skills
- 读取对应 SKILL.md 后执行

当前支持读取的 skills：
```bash
read workspace/skills/openclaw-superpowers/[skill-name]/SKILL.md
```
