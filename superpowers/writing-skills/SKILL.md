---
name: writing-skills
description: 当需要创建新 skill、编辑现有 skill、验证 skill 有效性时使用 — Skill 编写方法论。
---

# Writing Skills

## 核心原则

**Writing Skills = TDD 应用于流程文档。**

Skill 编写遵循 RED-GREEN-REFACTOR 循环：

| TDD 概念 | Skill 创建 |
|----------|-----------|
| Test case | 压力场景（用子代理测试） |
| 生产代码 | Skill 文档 (SKILL.md) |
| 红（失败） | 没有 skill 时代理违规（基线行为） |
| 绿（通过） | 有 skill 后代理遵循 |
| 重构 | 堵漏洞同时保持合规 |
| 先写测试 | 先运行基线场景再写 skill |
| 观察失败 | 记录代理的具体借口 |
| 最小代码 | 写 skill 针对具体违规 |
| 观察通过 | 验证代理现在合规 |
| 重构循环 | 发现新借口 → 堵住 → 重新验证 |

---

## 什么是 Skill

Skill 是一个技术的参考指南，帮助未来的 AI 实例找到并应用有效的方法。

**Skill 是：**
- 可复用的技术
- 模式和方法
- 参考指南

**Skill 不是：**
- 一次性问题的解决方案
- 标准实践（其他地方已有文档）
- 项目特定的约定（放在 CLAUDE.md）

---

## 何时创建 Skill

**创建：**
- 这个技术对你来说不是直觉上显而易见的
- 你会在不同项目中参考
- 模式应用广泛（不是项目特定的）
- 其他人也会受益

**不创建：**
- 一次性的解决方案
- 标准实践（有其他文档）
- 项目特定约定
- 可自动化执行的机械约束

---

## Skill 类型

### 1. Technique（技术）
有具体步骤的方法（调试、系统化流程）

### 2. Pattern（模式）
思考问题的方式（思维框架）

### 3. Reference（参考）
API 文档、语法指南、工具文档

---

## 目录结构

```
skills/
  skill-name/
    SKILL.md              # 主参考（必需）
    supporting-file.*     # 仅在需要时
```

**扁平命名空间** — 所有 skills 在同一可搜索空间

---

## SKILL.md 结构

### Frontmatter（YAML）

必需字段：
- `name`：只用字母、数字、连字符
- `description`：第三人称，描述**何时使用**（不是做什么）

```markdown
---
name: my-skill-name
description: Use when [具体触发条件和场景]
---

# My Skill Name

## Overview
这是什么？1-2 句话核心原则。

## When to Use
[症状和场景列表]

## Core Pattern
核心模式/步骤

## Quick Reference
快速参考表

## Common Mistakes
常见错误 + 修复

## Implementation
实现细节或链接
```

---

## Skill 描述字段优化

**关键：描述 = 何时使用，不是技能做什么**

❌ 不好：`"Skill that helps write code"`
✅ 好：`"Use when you need to write a new skill from scratch"`

**描述要回答：** "我应该现在读这个 skill 吗？"

---

## TDD 流程用于 Skill 创建

### Step 1: 红 — 基线测试

在写 skill 之前，先用子代理运行场景：

```
模拟一个需要这个 skill 的场景
    ↓
没有 skill 的情况下执行
    ↓
观察代理如何失败/违规
    ↓
记录具体的借口和违规模式
```

### Step 2: 绿 — 写最小 Skill

基于观察到的违规，写 skill：

```
针对具体违规写 skill
    ↓
只解决观察到的问题
    ↓
不要过度工程
```

### Step 3: 重构 — 堵漏洞

验证后，发现新漏洞：

```
运行更多压力测试
    ↓
发现新的借口模式
    ↓
添加到 skill
    ↓
重新验证
```

---

## 示例：创建 "有效提问" Skill

### Step 1: 红

**场景：** 用户说"帮我优化这个代码"

**没有 skill 的基线行为：**
```
代理：直接开始优化
借口："我知道该怎么做"
结果：可能不是用户真正想要的
```

### Step 2: 绿

**Skill：**
```markdown
## When to Use
用户说"帮我做XX"时

## 不要直接执行
先问：真正要解决的是什么？
```

### Step 3: 重构

压力测试后发现：

```
用户："帮我优化性能"
代理：先问"哪个部分的性能？"
新漏洞：没有问预算和优先级
添加："问清楚约束和优先级"
```

---

## 常见错误

| 错误 | 问题 | 正确做法 |
|------|------|----------|
| 不先测试 | 不知道 skill 是否有效 | 先运行基线场景 |
| 写太泛 | 代理还是找不到借口 | 具体触发条件 |
| 写太细 | 变成使用手册 | 原则 + 参考 |
| 跳过重构 | 漏洞没堵住 | 多次压力测试 |

---

## 整合 OpenClaw

### 读取 Skill

当需要使用 skill 时：

```bash
读取 workspace/skills/[skill-name]/SKILL.md
```

### 创建新 Skill

```bash
创建目录：workspace/skills/[skill-name]/
创建文件：workspace/skills/[skill-name]/SKILL.md
```

### Skill 命名

- ✅ `my-new-skill`
- ✅ `todo-tracking`
- ❌ `My New Skill`（有空格）
- ❌ `todo_tracking`（下划线）
- ❌ `my.new.skill`（有点）

---

## 验证清单

创建 skill 后验证：

- [ ] 运行过基线测试（没有 skill 的行为）？
- [ ] 记录了具体违规模式？
- [ ] Skill 解决了观察到的违规？
- [ ] 运行过压力测试？
- [ ] 描述字段回答"何时使用"？
- [ ] 放在正确的目录？
