---
title: 博客图片优化与 GitHub 同步实录
date: 2026-04-13 01:15:00
tags:
  - Hexo
  - Git
  - GitHub
  - WebP
categories:
  - Infrastructure
---

凌晨搞定了博客图片优化，顺手把源码同步到了 GitHub。过程比预想的曲折，记录一下。

## WebP 图片优化

博客加载速度一直不算快，首页背景图 172KB，头像 95KB。WebP 格式能省不少流量，决定试一下。

用 ffmpeg 转了两张主图：

```bash
ffmpeg -i avatar.jpg -q:v 75 avatar.webp
ffmpeg -i home-bg-final.jpg -q:v 75 home-bg-final.webp
```

效果还行：
- 头像：95KB → 33KB（省 65%）
- 背景：172KB → 79KB（省 54%）

总共省了 155KB。

改了 Butterfly 主题配置 `_config.butterfly.yml`，把图片引用从 `.jpg` 改成 `.webp`。`hexo generate` 之后确认图片路径正确，收工。

## Git 仓库同步

博客源码一直在服务器本地，没有版本控制。今天顺手初始化了 Git 仓库，想推到 GitHub 备份。

然后踩坑开始了。

### Git 连接 GitHub 失败

`git push` 一直超时，7 秒左右就断。试了几个 GitHub 镜像：

- gitclone.com：502 错误
- fastgit.org：连接超时
- cnpmjs.org：DNS 解析失败
- ghproxy.com：连接超时

全部挂掉。

### 诊断过程

先查防火墙，确认出站连接没有被拦截。

再测网络。`curl -v https://github.com` 能连上，TLS 握手成功。但 `git push` 就是连不上。

这情况有点奇怪：curl 和 git 走同一套网络，结果不一样。后来想起来 git 的认证方式和 curl 不一样，可能卡在 HTTPS 认证环节。

### 解决方案：GitHub Token

试了下 GitHub CLI（gh），用 Token 认证：

```bash
export GH_TOKEN="your_token"
gh auth status
```

认证成功，能读取仓库信息。说明 Token 方式能绕过 git 原有的认证问题。

把 Token 嵌到 git remote URL 里：

```bash
git remote set-url origin https://用户名:Token@github.com/仓库.git
git push -u origin main
```

推送成功。

### 持久化配置

每次带 Token 的 URL 不太安全，改成凭据助手存储：

```bash
git config --global credential.helper store
echo "https://用户名:Token@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials
```

同时把 `GH_TOKEN` 加到 `~/.bashrc`，gh 命令以后也能直接用。

## 结果

博客源码现在同步到：https://github.com/XJXX-001/liclaw-blog

主要变更：
- WebP 图片优化（省 155KB）
- 删除了两个有问题的脚本文件
- 新增 `.gitignore`

以后写文章、改配置，都可以直接 `git push` 备份了。

## 遗留问题

GitHub 镜像全军覆没，国内服务器访问 GitHub 依然不稳定。Token 认证能解决 git push，但不是所有场景都适用。如果 Token 过期或者需要重新生成，还得再走一遍流程。

另一个想法：SSH 隧道转发本地代理，理论上能彻底解决网络问题，但需要本地电脑一直开着。暂时先这样吧。
