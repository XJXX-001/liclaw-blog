---
title: 'TD-AI 四层记忆系统详解：如何让 AI 拥有"第二大脑"'
date: 2026-04-08 13:00:00
slug: tdai-memory-system
tags:
  - OpenClaw
  - AI
  - Memory
  - Local-First
categories:
  - AI Engineering
---

## 概述

[@tdai/memory-tdai](https://github.com/tdai) 是一个运行在 [OpenClaw](https://github.com/openclaw/openclaw) 上的四层本地记忆系统插件。核心特性：**完全离线**、**四层渐进式提炼**、**零外部依赖**，通过 LLM 将对话原始数据逐层抽象为结构化记忆、场景块和用户画像。

本文深入解析其核心机制，源代码级解读。

---

## 整体架构

```
对话结束
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  L0 Capture    对话录制      SQLite vec0 + JSONL 双写    │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  L1 Extraction  记忆提取      本地 LLM → 场景切分+去重    │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  L2 Scene       场景归纳      叙事文档 · Markdown        │
└────────────────────┬──────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  L3 Persona     用户画像      persona.md                 │
└─────────────────────────────────────────────────────────┘

对话开始（Auto-Recall）
    │
    ▼
 Hybrid 搜索 → 召回相关 L1 记忆
 + 加载 persona.md + scene_blocks
 → 注入 Agent 上下文
```

---

## L0：对话录制

**目标**：原始捕获每轮对话消息，零丢失。

### 双写机制

L0 recorder 同时写入两个存储：

| 存储 | 路径 | 用途 |
|------|------|------|
| SQLite vec0 | `vectors.db` | 向量搜索（可选） |
| JSONL | `conversations/*.jsonl` | 原始消息持久化 |

```typescript
// 对话消息结构
interface ConversationMessage {
  id: string;           // 全局唯一消息ID
  role: "user" | "assistant";
  content: string;      // 原始文本
  timestamp: number;    // Unix ms
  sessionKey: string;   // 会话标识
}
```

### 质量门控（Quality Gate）

L0 **不做过滤**（全部捕获），L1 阶段才执行严格过滤：

```typescript
// L1 质量门控规则
function shouldExtractL1(content: string): boolean {
  // 过滤：纯符号、太短、prompt injection 等
}
```

这是设计选择：**录制端保真，提取端严控**。

### 原子性写入（Checkpoint + 文件锁）

`auto-capture.ts` 使用文件锁防止并发写入导致重复记录：

```typescript
await checkpoint.captureAtomically(sessionKey, pluginStartTimestamp, async (afterTimestamp) => {
  // 1. 读取当前游标
  // 2. 写入新消息
  // 3. 更新游标（原子）
});
```

---

## L1：记忆提取

**目标**：从 L0 原始对话中，用本地 LLM 提炼出结构化记忆片段。

### 核心设计：一趟 LLM 调用完成两件事

`l1-extractor.ts` 的 `callLlmExtraction` 函数，一次 LLM 调用同时输出：

1. **情境切分**（Scene Segmentation）：将对话按话题边界分段
2. **记忆提取**：每段提取多条结构化记忆

### 提示词工程（Prompt 核心逻辑）

L1 提取提示词（`l1-extraction.ts`）定义了严格的输出规范：

```typescript
// 支持提取的三大类型
type MemoryType = "persona" | "episodic" | "instruction";

// 提取句式规范
// persona:  "用户（姓名）喜欢/是/擅长..."
// episodic: "用户（姓名）在 [时间] 于 [地点] [做了某事]"
// instruction: "用户要求/希望 AI 以后回答时..."
```

**时间建模**：episodic 记忆支持两种时间标注：

```json
{
  "metadata": {
    "activity_start_time": "2026-04-08T10:00:00.000Z",
    "activity_end_time": "2026-04-08T12:00:00.000Z"
  }
}
```

- `activity_start_time` + `activity_end_time`：段时间（活动持续期）
- 两者皆无时：回退使用 L0 的 message timestamp 作为点时间

### 冲突检测（Batch Dedup）

提取后的记忆通过向量相似度做冲突检测（`l1-dedup.ts`）：

**三段降级策略**：

```
1. Vector Recall（向量召回）→ cosine similarity  Top-K 候选
2. FTS5 BM25（关键词召回）→ 无向量引擎时的降级
3. 跳过去重 → 直接存储（向量/FTS 均不可用时）
```

```typescript
// 冲突决策类型
type DedupDecision =
  | { action: "store"; target_ids: [] }           // 新增
  | { action: "update"; target_ids: [existingId] } // 更新已有
  | { action: "discard"; target_ids: [] }         // 丢弃（重复）
```

### 场景连续性

`previousSceneName` 参数实现跨批次上下文连续：

```typescript
// 提取提示词模板
`【上一个情境】：${previousSceneName}

// 【待提取的新消息】
// ...
```

---

## L2：场景归纳

**目标**：将 L1 碎片记忆融合为连贯的叙事文档（Scene Block）。

### 核心原则：不是清单，是叙事

场景文件不是记忆列表，而是**连贯段落**。这是 L2 和 L1 的本质区别：

| 层级 | 形态 | 单位 |
|------|------|------|
| L1 | JSONL 片段 | 单条记忆 |
| L2 | Markdown 叙事文档 | 场景（多条相关记忆融合） |

### 场景文件格式

```markdown
-----META-START-----
created: 2026-04-06T10:00:00Z
updated: 2026-04-08T12:00:00Z
summary: 博客系统部署与内容增长策略
heat: 79
-----META-END-----

## 用户核心特征
用户在后端开发方面表现出对静态网站的强烈偏好...（连贯段落）

## 核心叙事
本周用户主要在搭建 Hexo 博客系统...（Trigger → Action → Result 叙事弧线）

## 演变轨迹
- [2026-04-07]: 确立内容增长目标：日均 PV 500
```

### 热力管理（Heat）

每条场景记录 `heat` 值，驱动更新优先级：

| 操作 | heat 变化 |
|------|----------|
| 新建 | `heat = 1` |
| 更新 | `heat = 旧值 + 1` |
| 合并 | `heat = sum(所有相关) + 1` |

场景数量上限 **15 个**。达到上限时强制合并最低热度场景。

### LLM 驱动的场景操作

`scene-extractor.ts` 使用 `read_file` + `write_to_file` / `replace_in_file` 让 LLM 直接操作 Markdown 文件。LLM 输出中的 `[PERSONA_UPDATE_REQUEST]` 信号触发 persona 更新。

---

## L3：用户画像

**目标**：基于 L2 场景块，生成/更新 `persona.md`。

### 触发条件

每 N 条新记忆触发一次画像生成（默认 N = 50）。

### Persona 文件结构

```markdown
# User Narrative Profile

> **Archetype**: [用户原型描述]

> **基本信息**
- 姓名：
- 网站：
- 云资源：

## Chapter 1: Context & Current State
[当前情境快照]

## Chapter 2: The Texture of Life
[行为偏好、审美标准]

## Chapter 3: Interaction & Cognitive Protocol
[沟通策略、决策逻辑]

## Chapter 4: Deep Insights & Evolution
[深层洞察、演变轨迹]
```

### 备份机制

每次更新前自动备份，保留最近 3 个版本（`scene_backupCount: 10`）。

---

## Auto-Recall：记忆召回

**目标**：对话开始前，将相关记忆注入 Agent 上下文。

### 召回管线

```typescript
async function performAutoRecall({ userText, ... }) {
  // 1. L1 搜索（用户意图匹配）
  const memoryLines = await searchMemories(userText);

  // 2. L3 persona 加载
  const persona = await readPersona();

  // 3. L2 scene navigation（全量注入，LLM 判断相关性）
  const sceneNav = await generateSceneNavigation();

  // 4. 组装为 appendSystemContext
  return { appendSystemContext: [...persona, ...sceneNav, ...memories, toolsGuide] };
}
```

### 三种搜索策略

| 策略 | 原理 | 适用场景 |
|------|------|---------|
| `keyword` | FTS5 BM25 关键词匹配 | 无向量引擎 |
| `embedding` | 向量余弦相似度 | 有本地/远程 embedding |
| `hybrid`（默认） | 关键词 + 向量 **RRF 融合** | 两者兼备 |

### RRF（Reciprocal Rank Fusion）融合

```typescript
// RRF 公式：score = Σ 1 / (k + rank_i)
// k = 60（常数）
const RRF_K = 60;

function rrfScore(rank: number): number {
  return 1 / (RRF_K + rank + 1);
}
```

关键词和向量两个排序列表，按 RRF 分数加权融合——同时命中两条检索路径的记忆得分更高。

### 记忆格式化（Prompt 注入格式）

```typescript
// 输出示例
`- [persona] 用户叫王小明，30岁，是一名软件工程师。

- [episodic|博客建站] Hexo + Butterfly v5.5.4 部署完成。(活动时间: 2026-04-06)

- [instruction] 用户要求回答时使用中文，保持简洁直接。
```

---

## 向量引擎：sqlite-vec

**存储**：`vectors.db`（SQLite + vec0 扩展）

**支持的操作**：

```sql
-- 向量存储（L0 和 L1 双重索引）
CREATE VIRTUAL TABLE vectors USING vec0(
  embedding float[768]
);

-- KNN 查询
SELECT * FROM vectors WHERE embedding MATCH ?
  ORDER BY distance;
```

**本地 embedding**：使用 `node-llama-cpp` 加载 GGUF 模型（首次运行自动下载），完全离线。

---

## 与 Builtin Memory 的区别

| 维度 | Builtin Memory | memory-tdai |
|------|---------------|-------------|
| 架构 | `MEMORY.md` + SQLite | 四层 L0→L1→L2→L3 管线 |
| 提取方式 | 手动写入 | 自动 LLM 提取 |
| 向量 | 可选 | sqlite-vec + 本地 GGUF |
| 用户画像 | 无 | persona.md 完整画像 |
| 场景归纳 | 无 | 叙事型 Scene Block |

---

## 总结

memory-tdai 的核心设计哲学：**本地优先、LLM 驱动、四层渐进提炼**。

- **L0** 原始保真，零丢失
- **L1** 结构化抽象，质量门控 + 向量去重
- **L2** 叙事融合，热力管理驱动演化
- **L3** 用户画像，跨场景归纳

整个系统无需任何外部 API，所有数据留在本地，是真正意义上的"私有第二大脑"。
