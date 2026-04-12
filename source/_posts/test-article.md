---
title: Hexo 配置技巧
date: 2026-04-06 18:02:00
slug: hexo-butterfly-tips
tags:
  - Hexo
  - 配置
categories:
  - Infrastructure
---

## 前言

本文记录 Hexo 博客系统的常用配置技巧，涵盖主题定制、URL 优化、性能提升等方面。

## 1. 永久链接配置

在 `_config.yml` 中设置文章 URL 结构，避免中文路径：

```yaml
# _config.yml
permalink: :year/:month/:day/:slug/
```

文章文件名即 slug，无需中文：

```bash
hexo new "hexo-tips"  # 生成 hexo-tips.md
# URL: /2026/04/06/hexo-tips/
```

## 2. 主题配置管理

推荐将主题配置独立为 `_config.butterfly.yml`，避免升级主题时丢失个性化设置：

```yaml
# _config.butterfly.yml
# 复制 hexo-theme-butterfly/_config.yml 内容到此文件
# 仅修改需要个性化的配置项
```

## 3. 自定义主题色

通过 `theme_color` 节点配置全局配色方案：

```yaml
# _config.butterfly.yml
theme_color:
  enable: true
  main: "#5E6AD2"        # 主色调
  paginator: "#5E6AD2"    # 分页器
  button_hover: "#4B5AC7" # 按钮悬停
  link_color: "#5E6AD2"   # 链接色
```

## 4. 目录 TOC 进度条

文章内嵌目录模块，支持滚动进度指示：

```yaml
# _config.butterfly.yml
toc:
  post: true        # 文章页显示目录
  page: false       # 独立页面不显示
  number: true      # 显示章节编号
  expand: false     # 默认折叠状态
  scroll_percent: true  # 显示滚动进度
```

## 5. 代码高亮配置

Hexo 内置 highlight.js，支持代码块语法高亮：

```yaml
# _config.yml
highlight:
  line_number: true
  auto_detect: false
  tab_replace: '  '  # 2空格缩进
  hljs: false
```

## 6. 部署命令

生成静态文件并部署到 Web 目录：

```bash
# 生成
hexo generate

# 复制到 Web 目录（示例路径）
cp -r public/* /var/www/yoursite/blog/

# 或使用 rsync 增量同步
rsync -avz --delete public/ /var/www/yoursite/blog/
```

## 7. 常用插件

```bash
# 搜索支持
pnpm add hexo-generator-search

# RSS 订阅
pnpm add hexo-generator-feed

# Sitemap
pnpm add hexo-generator-sitemap
```

## 8. 目录结构

```
blog/
├── _config.yml          # Hexo 主配置
├── _config.butterfly.yml # 主题配置（独立文件）
├── source/
│   ├── _posts/         # 文章目录
│   ├── tags/           # 标签页
│   └── categories/     # 分类页
├── public/             # 生成的静态文件
└── node_modules/       # 依赖
```

## 总结

Hexo 的核心优势在于：纯静态文件、无数据库、Markdown 写作、版本可控。以上技巧能帮助快速搭建并维护一个专业博客。
