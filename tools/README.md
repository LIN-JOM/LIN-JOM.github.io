# tools/

本地辅助脚本，**不属于站点内容**，GitHub Actions 构建时会忽略（`tools/` 不在 Jekyll 的发布范围内）。

## preview.py

在没有 Ruby / Jekyll 的机器上，把站点渲染成静态 HTML，用来检查排版和配色。

```bash
python tools/preview.py
```

输出到 `_preview/`，用浏览器打开 `_preview/index.html` 即可。

它做三件事：

1. 读取真实的 `_posts/*.md`、`assets/style.css` 和站点信息；
2. 用一份简化的 Markdown 渲染器（支持标题、段落、列表、粗体、行内代码、代码块、链接）生成 HTML；
3. 按 `_layouts/` 的结构拼出首页、关于页和每篇文章。

注意：这是**预览工具**，不是构建系统。真正发布出去的 HTML 由 GitHub Actions 上的 Jekyll 生成，两者排版细节可能略有差异。
