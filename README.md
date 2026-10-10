# Markdown 个人博客模板

这是一个不需要 Node.js、npm 或 React 的 Jekyll 静态博客模板。

## 学生开箱步骤

1. 打开模板仓库，点击 **Use this template → Create a new repository**。
2. 填写自己决定的仓库名称和公开/私有可见性。
3. 创建完成后，进入自己仓库的 **Settings → Pages**，把 Source 设为 **GitHub Actions**。
4. 等待 `Build and deploy Jekyll site` workflow 完成，再打开 Pages URL。
5. 修改 `_config.yml` 中的名字，编辑 `index.html` 的项目卡片，并在 `_posts/` 中写自己的 Markdown 文章。

仓库创建和 Pages 设置也可以让 Agent 操作，但必须先把目标仓库 URL 明确告诉 Agent，并在推送前检查 `git diff`。

注意：仓库里的 `index.html` 是 Jekyll 模板源码，不能靠双击本地文件看到最终页面；最终 HTML 会由 GitHub Actions 生成。学生不需要在电脑上安装 Ruby、Jekyll、Node.js 或 npm。

## 写一篇新文章

在 `_posts/` 中复制示例文章，文件名使用：

```text
YYYY-MM-DD-title.md
```

文章开头保留 Front Matter：

```yaml
---
layout: post
title: 文章标题
date: 2026-10-08
excerpt: 一句话摘要
tags:
  - 学习
---
```

第二个 `---` 之后直接写 Markdown 正文：标题、段落、列表、链接、代码块都可以使用。

## 发布流程

1. 修改或新增 `_posts/*.md`。
2. 修改首页内容时编辑 `index.html`。
3. 修改关于页时编辑 `about.md`。
4. 修改配色和排版时编辑 `assets/style.css`。
5. 在浏览器中检查文件内容和链接。
6. `git diff` 检查变更。
7. `git add`、`git commit`、`git push`。
8. GitHub Actions 自动运行 Jekyll，将 Markdown 编译成 HTML 并发布到 GitHub Pages。

## 第一次启用 Pages

把仓库推送到 GitHub 后，在仓库中打开：

```text
Settings → Pages → Source → GitHub Actions
```

之后每次推送到 `main`，workflow 都会重新生成网站。

## 需要学生理解的概念

```text
Markdown 文章
      ↓
Jekyll / GitHub Actions
      ↓
HTML 页面
      ↓
GitHub Pages URL
```

学生不需要在本地安装 Ruby、Jekyll、Node.js 或 npm。构建发生在 GitHub Actions 上。

## Agent 提示词

```text
/goal 这是一个 Jekyll 静态博客项目。请先读取 README、_config.yml、index.html、_layouts 和 _posts。
以后新增文章时，只在 _posts/ 中创建 YYYY-MM-DD-title.md，并使用现有 Front Matter 和 layout: post。
不要引入 React、Vue、Node.js、npm、外部 CDN 或新的构建工具。
修改前先列出文件和计划；修改后检查 Markdown Front Matter、文章链接、相对资源路径和 Git diff。
我确认目标仓库后，才执行 git commit 和 git push。
```
