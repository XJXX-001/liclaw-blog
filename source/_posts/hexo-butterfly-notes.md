---
title: Hexo + Butterfly 部署笔记
date: 2026-04-06 18:18:00
slug: hexo-butterfly-notes
tags:
  - Hexo
  - Butterfly
  - 部署
categories:
  - Infrastructure
---

> 记录一次从零搭建 Hexo 博客的全过程，涵盖选型、配置、踩坑经验。

## 背景

选择 Hexo + Butterfly 主题，目标是快速上线、便于维护、不依赖外部平台。

## 关键步骤

### 1. 安装 Hexo

```bash
npm install -g hexo@latest
hexo init blog
cd blog
npm install
```

### 2. 安装 Butterfly 主题

推荐使用 NPM 安装：

```bash
pnpm add hexo-theme-butterfly
```

**必装依赖**：
```bash
pnpm add hexo-renderer-pug hexo-renderer-stylus
pnpm add hexo-generator-search hexo-generator-feed hexo-generator-sitemap
pnpm add hexo-wordcount
```

### 3. 配置管理

**禁止直接修改主题源码**，在 Hexo 根目录创建 `_config.butterfly.yml`，复制主题配置到此处。升级主题时不会丢失个性化设置。

### 4. 常见配置

**Footer 版权**：
```yaml
footer:
  owner:
    enable: false      # 移除默认版权信息
  copyright:
    enable: false
  custom_text: 自定义文本
```

**主题色**：
```yaml
theme_color:
  enable: true
  main: "#5E6AD2"
```

### 5. 特殊页面

```bash
hexo new page tags
hexo new page categories
hexo new page search
```

### 6. 发布流程

```bash
hexo clean
hexo generate
cp -r public/* /path/to/webroot/
```

## 踩坑记录

| 坑 | 原因 | 解决 |
|----|------|------|
| 主题安装失败 | npm 兼容问题 | 改用 pnpm |
| 脚本加载失败 | 缺少 hexo-util、moment-timezone | 补装依赖 |
| YAML 重复 key | sed 替换逻辑问题 | 用 Python 替代 |
| TOC 高亮色无配置接口 | CSS 硬编码 | inject 覆盖 |
| theme_config 不生效 | 深度合并问题 | 直接改配置文件 |

## URL 优化

文件名即 slug，用英文命名：

```
source/_posts/my-article.md
# URL: /2026/04/06/my-article/
```

## 总结

Hexo + Butterfly 组合成熟稳定，配置项丰富。核心要点：

1. 不要改源码，用独立配置文件
2. 必装依赖一次性装齐
3. YAML 修改用 Python 比 sed 更安全
4. 发布后检查 HTTP 状态码

适合个人博客、技术文档、项目演示等场景。
