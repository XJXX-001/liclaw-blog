---
name: openclaw-superpowers
description: OpenClaw 版 Superpowers — AI 编程超能力框架入口。任何人机协作任务前必读。
---

# 🦐 OpenClaw Superpowers

**Superpowers for OpenClaw — 让 AI 真正会干活**

---

## 核心理念

当你接到一个任务时：

1. **不要急着动手** — 先问清楚"真正要做什么"
2. **先想后做** — 制定计划再执行
3. **小步快跑** — 把大任务拆成小块
4. **持续验证** — 每个步骤完成后验证
5. **人类确认** — 关键节点让人类把关

---

## 指令优先级

1. **用户的明确指令**（AGENTS.md、USER.md、直接需求）— 最高优先级
2. **Skills** — 覆盖默认行为
3. **系统默认** — 最低优先级

如果 AGENTS.md 说"不要用 TDD"但 skill 说"要用 TDD"，遵循用户指令。用户才是主人。

---

## 触发规则

**任何动作前，先检查是否有适用的 skill：**

```
收到用户消息
    ↓
是否有 skill 适用？（哪怕只有 1% 可能）
    ↓
有 → 读取并使用 skill
    ↓
无 → 直接执行
```

---

## Red Flags（停止标志）

这些想法意味着"你在找借口"：

| 想法 | 现实 |
|------|------|
| "这只是个小问题" | 问题再小也是任务，检查 skill |
| "我先收集点信息" | Skills 告诉你如何收集 |
| "我知道该怎么做" | 知道概念 ≠ 用了 skill |
| "不需要那么正式" | 如果 skill 存在，就用它 |
| "我先做这个" | 在做任何事之前检查 |
| "这感觉很有成效" | 无纪律的行动浪费时间 |

---

## Skill 类型

**刚性（必须严格遵循）：**
- TDD、调试、规划 — 不要适应，遵循它

**柔性（可灵活调整）：**
- 模式、原则 — 根据上下文适应

---

## 核心 Skills

| Skill | 用途 |
|-------|------|
| `brainstorming` | 需求构思和分析 |
| `writing-plans` | 制定实施计划 |
| `subagent-driven-development` | 子代理驱动执行 |
| `test-driven-development` | 测试驱动开发 |
| `systematic-debugging` | 系统化调试 |
| `verification-before-completion` | 完成前验证 |
| `finishing-a-development-branch` | 分支收尾 |

---

## 工作流

```
用户需求 → brainstorming（构思）→ writing-plans（计划）→ 执行 → 验证 → 完成
```

---

*This is the OpenClaw adaptation of Superpowers by obra (151k+ stars)*
