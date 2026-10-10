---
layout: post
title: 第一次看懂 GitHub Actions 是怎么发布网站的
date: 2026-10-07
excerpt: 推送之后网页自己更新了，我想搞清楚中间到底发生了什么。
tags:
  - GitHub Actions
  - 学习
---

第一次推送完等了一分钟，刷新网址，页面就变了。当时我觉得有点像魔法，所以去把 `.github/workflows/pages.yml` 从头读了一遍。

读完发现它其实很好懂。

## 触发条件

```yaml
on:
  push:
    branches: ["main"]
  workflow_dispatch:
```

意思是：**只要 `main` 分支有推送就跑**。下面那行 `workflow_dispatch` 允许我在网页上手动点一个按钮触发，调试的时候有用。

## 两个 job

workflow 里有两个任务，第二个依赖第一个：

```text
build  →  deploy
```

`build` 做三件事：把我的仓库克隆到一台 Ubuntu 机器上、用 Jekyll 把 Markdown 编译成 HTML、把结果打包成一个 artifact 上传。

`deploy` 把这个 artifact 交给 GitHub Pages 发布出去。

## 权限那一块

有一处我一开始看不懂：

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

现在我的理解是：workflow 默认能做的事被限制住了，这里显式声明它只需要**读代码、写 Pages、用 OIDC 令牌换取部署权限**。特别是 `id-token: write`，它让 GitHub 用短期令牌完成部署，而不需要我手动配一个长期密钥——这比把密钥存在仓库变量里安全。

## 一个实际的教训

我改配色的时候推送了一次，但页面没变。

排查下来不是 workflow 的问题，而是**部署有缓存**，多等了一会儿就好了。这件事提醒我：看到「Actions 显示绿色」和「浏览器看到新页面」之间，还隔着一次发布和一层缓存。

## 现在的发布流程

```bash
git add .
git commit -m "写一篇新文章"
git push
```

之后什么都不用做。对我来说，这是「发布」这件事应该有的样子——它不该是一个我需要专门学习的操作。
