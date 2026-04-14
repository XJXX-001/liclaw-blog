---
name: test-driven-development
description: 实现任何功能时使用 — 遵循红、绿、重构循环，确保测试覆盖。
---

# Test-Driven Development (TDD)

## 核心循环

```
红 → 绿 → 重构

红：写一个失败测试
绿：写最小代码让测试通过
重构：改善代码，测试保持通过
```

## 步骤

### Step 1: 红 — 写失败测试

**在写任何实现代码之前，先写测试。**

```python
def test_feature_behavior():
    """测试：功能 X 应该在 Y 情况下产生 Z 结果"""
    # Arrange - 设置测试数据
    input_data = something
    
    # Act - 执行被测功能
    result = feature_function(input_data)
    
    # Assert - 验证结果
    assert result == expected
```

### Step 2: 绿 — 写最小实现

**只写让测试通过的代码，不要多想。**

```python
def feature_function(input_data):
    return expected  # 最简单的实现
```

### Step 3: 重构 — 改善代码

测试通过后：
- 消除重复
- 改善命名
- 简化逻辑
- 确保测试仍然通过

## 测试原则

### Arrange-Act-Assert (AAA)

每个测试清晰的三段式：

```python
# Arrange - 准备
user = create_test_user()

# Act - 执行
result = user.update_profile(name="New Name")

# Assert - 验证
assert result.name == "New Name"
```

### 一个测试，一个断言（尽量）

```python
# 好：一个测试测一件事
def test_user_name_updated():
    user = create_test_user()
    user.update_name("Alice")
    assert user.name == "Alice"

def test_user_email_updated():
    user = create_test_user()
    user.update_email("alice@example.com")
    assert user.email == "alice@example.com"

# 可接受：多个相关断言
def test_user_full_update():
    user = create_test_user()
    user.update(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

### 测试的是行为，不是实现

```python
# 不好：测试实现细节
def test_internal_cache_used():
    assert len(internal_cache) > 0

# 好：测试外在行为
def test_duplicate_request_returns_cached_result():
    result1 = fetch_data("key")
    result2 = fetch_data("key")
    assert result1 is result2  # 同一对象（缓存）
```

## 测试命名

```python
# 格式：test_<功能>_<场景>_<预期>
def test_user_login_with_correct_password_succeeds():
    ...

def test_user_login_with_wrong_password_fails():
    ...

def test_cart_total_with_multiple_items_calculates_correctly():
    ...
```

## 常见反模式

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| 无测试 | 无法验证 | 先写测试 |
| 过度 mock | 测试不是真实场景 | 使用真实依赖或简化依赖 |
| 测试实现 | 实现变测试就挂 | 测试行为 |
| 随机数据 | 测试不稳定 | 使用固定测试数据 |
| 全局状态 | 测试间互相影响 | 隔离测试 |

## 在子代理开发中使用 TDD

实现每个任务时：

1. **读取 task spec**
2. **写失败测试**
3. **运行测试，确认失败**
4. **写最小实现**
5. **运行测试，确认通过**
6. **重构（如需要）**
7. **提交**

## 调试失败测试

```
测试失败了？
    ↓
读错误信息
    ↓
是实现 bug？
    ↓ 是 → 修复实现
    ↓ 否
是测试 bug？
    ↓ 是 → 修复测试
    ↓ 否
是理解偏差？
    ↓ 是 → 澄清 spec
```

## 原则提醒

- **YAGNI** — 不需要的功能不要测试
- **DRY** — 测试代码也要 DRY，但测试隔离优先
- **快速反馈** — 测试要能快速运行
- **独立** — 每个测试独立运行，不依赖其他测试
