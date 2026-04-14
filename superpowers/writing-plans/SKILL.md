---
name: writing-plans
description: 当有明确需求/规格说明，需要制定实施计划时使用 — 在动手前产出详细的执行计划。
---

# Writing Plans

## 触发条件

有了明确的需求规格说明（Spec）后，制定实施计划。

## 核心原则

**假设执行者：**
- 是合格的开发者
- 但完全不了解你的代码库
- 不了解你的技术选型
- 不太懂测试设计

**因此计划要完整、精确、无歧义。**

## Plan 文档格式

```markdown
# [功能名称] 实施计划

**Skill 提示：** 使用 subagent-driven-development（推荐）或 executing-plans 执行此计划。

---

## 目标
一句话描述

## 架构方案
2-3 句话描述技术方案

## 技术栈
关键技术和依赖

---

## 文件结构

```
src/
├── 文件1.py      # 职责：XXX
├── 文件2.py      # 职责：XXX
tests/
├── test_文件1.py
docs/
└── README.md
```

**设计原则：**
- 每个文件单一职责
- 文件变更要一起的放一起
- 遵循既有模式

---

## 任务列表

### Task 1: [组件名称]

**文件：**
- 创建：`src/path/to/file.py`
- 修改：`src/path/existing.py:123-145`
- 测试：`tests/path/test.py`

- [ ] **Step 1: 写失败测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: 运行测试验证失败**

命令：`pytest tests/path/test.py::test_name -v`
预期：FAIL with "function not defined"

- [ ] **Step 3: 写最小实现**

```python
def function(input):
    return expected
```

- [ ] **Step 4: 运行测试验证通过**

命令：`pytest tests/path/test.py::test_name -v`
预期：PASS

- [ ] **Step 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

---

### Task 2: [下一个组件]

...

```

## 任务粒度

**每个 step 1-5 分钟完成：**
- "写失败的测试" = 1 step
- "运行测试验证失败" = 1 step
- "写最小实现" = 1 step
- "运行测试验证通过" = 1 step
- "提交" = 1 step

## 禁止事项

**永远不要写：**
- ❌ "TBD"、"TODO"、"后面再填"
- ❌ "添加适当的错误处理"
- ❌ "测试一下"
- ❌ "参考 Task N"（重复代码）
- ❌ 描述性步骤（必须有具体命令和代码）

## 自检清单

完成后自己检查：

**1. Spec 覆盖检查：**
- 逐条过 spec，每条都能找到对应 task
- 列出任何遗漏

**2. 占位符扫描：**
- 搜索"TBD"、"TODO"、"后面再填"
- 修复所有占位符

**3. 类型一致性：**
- Task 3 的函数名 = Task 7 的函数名吗？
- 类型、签名都一致吗？

发现问题就修复，不用重新 review。

## 交付

计划完成后：

```
计划已保存至：`memory/plans/YYYY-MM-DD-feature-name.md`

两种执行方式：

1. 子代理驱动（推荐）— 每个 task 派发独立子代理，快速迭代
2. 顺序执行 — 在当前会话顺序执行，带检查点

选择哪种？
```

## 使用 subagent-driven-development

如果选择子代理驱动：
- 必须使用 `sessions_spawn` 派发子代理
- 每个 task 后做两阶段 review：spec 合规 → 代码质量
- 保持主会话专注于协调
