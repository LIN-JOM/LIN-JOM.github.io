---
layout: post
title: 用 Jekyll 和 GitHub Pages 搭一个不要构建工具的博客
date: 2026-10-05
excerpt: 从模板到可以访问的网址，记录我把这个博客搭起来的过程。
tags:
  - Jekyll
  - GitHub Pages
---

我想有一个属于自己的地方写东西，但又不想为了写一篇几百字的笔记，去维护一整套前端工具链。

最后我选了 Jekyll 加 GitHub Pages，整个过程比我预想的简单。

## 为什么是 Jekyll

原因很直接：**Markdown 文件就是文章本身**。

`_posts/2026-10-05-setup-blog.md` 这样一个文件，前面写上几行 front matter，后面正常写 Markdown，推送之后 GitHub 就会把它编译成 HTML 页面。

```yaml
---
layout: post
title: 文章标题
date: 2026-10-05
excerpt: 一句话摘要
tags:
  - Jekyll
---
```

我不用在本地装 Ruby，也不用跑 `jekyll build`。构建发生在 GitHub Actions 的服务器上，我的电脑只负责写文件。

## 数据是怎么流动的

```text
_posts/*.md  →  GitHub Actions  →  _site/*.html  →  我的博客网址
```

这个链条里没有一步需要我本机安装东西，这是我最满意的地方。

## 目前的结构

- `_config.yml` —— 站点标题、作者、网址这些全局设置
- `index.html` —— 首页，用 Liquid 循环把最近的文章列出来
- `_layouts/` —— 两个模板，`default.html` 管整体框架，`post.html` 管文章页
- `assets/style.css` —— 全部样式，配色集中在 `:root` 的 CSS 变量里
- `about.md` —— 关于页

## 下一步

我打算先把写作这件事坚持下来，格式和布局以后再说。工具已经足够简单了，不该再成为不动笔的理由。
