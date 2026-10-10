"""Render a static preview of the Jekyll blog (no Ruby needed).

Reads the real _posts/*.md, assets/style.css and the site config, and emits
plain HTML into _preview/ so the layout can be inspected in a browser.
This is a preview tool only - it is NOT part of the site build.
"""
import html
import os
import re

# 站点根目录是 tools/ 的上一级，脚本可以从任意位置运行
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(W, "_preview")


def load_config():
    """直接读 _config.yml，避免预览和真实站点配置不一致。"""
    cfg = {}
    fmt = None                      # 当前解析的是哪个多行块
    for line in open(os.path.join(W, "_config.yml"), encoding="utf-8"):
        line = line.rstrip("\n")
        if fmt:
            if line.startswith((" ", "\t")) and line.strip():
                cfg[fmt] += " " + line.strip()
                continue
            fmt = None
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith((">", "|")):
            cfg[key] = ""; fmt = key
        elif val:
            cfg[key] = val.strip('"').strip("'")
    return cfg


SITE = load_config()
NAME = SITE["title"].split("·")[0].strip()


def parse_front_matter(path):
    raw = open(path, encoding="utf-8").read()
    i = raw.find("\n---", 3)
    fm, body = raw[3:i], raw[i + 4:].strip()
    meta = {}
    for key in ("title", "date", "excerpt"):
        m = re.search(r"(?m)^%s:\s*(.+)$" % key, fm)
        meta[key] = m.group(1).strip() if m else ""
    m = re.search(r"(?ms)^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm)
    meta["tags"] = [t.strip() for t in re.findall(r"-\s*(.+)", m.group(1))] if m else []
    return meta, body


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def markdown(md):
    out, para, in_code = [], [], False
    list_tag = None

    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            para.clear()

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append("</%s>" % list_tag)
            list_tag = None

    for ln in md.split("\n"):
        if ln.startswith("```"):
            flush_para(); close_list()
            if not in_code:
                out.append("<pre><code>"); in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            continue
        if in_code:
            out.append(html.escape(ln, quote=False))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            flush_para(); close_list()
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl))
            continue
        m = re.match(r"^\s*-\s+(.*)$", ln)
        if m:
            flush_para()
            if list_tag != "ul":
                close_list(); out.append("<ul>"); list_tag = "ul"
            out.append("<li>%s</li>" % inline(m.group(1)))
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
        if m:
            flush_para()
            if list_tag != "ol":
                close_list(); out.append("<ol>"); list_tag = "ol"
            out.append("<li>%s</li>" % inline(m.group(1)))
            continue
        if not ln.strip():
            flush_para(); close_list()
            continue
        para.append(ln.strip())
    flush_para(); close_list()
    return "\n".join(out)


def page(title, body, depth=0):
    """Mirror of _layouts/default.html."""
    prefix = "../" * depth
    head_title = ("%s · %s" % (title, SITE["title"])) if title else SITE["title"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(SITE['bio'], quote=True)}">
  <title>{html.escape(head_title)}</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到主要内容</a>
  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="{prefix}index.html"><span class="brand-mark">✦</span> {html.escape(NAME)}</a>
      <nav aria-label="主导航">
        <ul class="nav-links">
          <li><a href="{prefix}index.html#writing">文章</a></li>
          <li><a href="{prefix}index.html#projects">项目</a></li>
          <li><a href="{prefix}about.html">关于我</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer"><div class="wrap footer-row"><span>© 2026 {html.escape(NAME)}</span><span><a href="https://github.com/{SITE['github_username']}">GitHub</a> · <a href="mailto:{SITE['email']}">Email</a></span></div></footer>
</body>
</html>
"""


def main():
    os.makedirs(os.path.join(OUT, "posts"), exist_ok=True)

    posts = []
    for fn in sorted(os.listdir(os.path.join(W, "_posts")), reverse=True):
        if not fn.endswith(".md"):
            continue
        meta, body = parse_front_matter(os.path.join(W, "_posts", fn))
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", fn[:-3])
        meta.update(body=body, file=fn, slug=slug)
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)

    # ---- index.html ----
    idx = open(os.path.join(W, "index.html"), encoding="utf-8").read()
    idx = idx[idx.find("\n---", 3) + 4:]
    idx = idx.replace("{{ 'now' | date: '%Y' }}", "2026")
    idx = re.sub(r"\{\{\s*site\.title\s*\|\s*split.*?\}\}", html.escape(NAME), idx)
    idx = re.sub(r"\{\{\s*site\.bio\s*\|.*?\}\}", html.escape(SITE["bio"]), idx)
    idx = idx.replace("{{ site.email }}", SITE["email"])
    idx = idx.replace("{{ site.github_username }}", SITE["github_username"])
    cards = []
    for p in posts[:6]:
        tag = " · " + p["tags"][0] if p["tags"] else ""
        ex = html.escape(p["excerpt"], quote=False)
        ex = ex[:100] + "…" if len(ex) > 100 else ex
        cards.append(
            '    <article class="card">\n'
            '      <div class="card-meta">%s%s</div>\n'
            "      <h3>%s</h3>\n"
            "      <p>%s</p>\n"
            '      <a class="card-link" href="posts/%s.html">阅读文章 →</a>\n'
            "    </article>" % (p["date"].replace("-", "."), tag,
                               html.escape(p["title"]), ex, p["slug"]))
    idx = re.sub(r"(?s)\{%\s*for post in site\.posts.*?\{%\s*endfor\s*%\}", "\n".join(cards), idx)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page("", idx))

    # ---- about.html ----
    _, ab = parse_front_matter(os.path.join(W, "about.md"))
    ab = ab.replace("{{ site.github_username }}", SITE["github_username"])
    ab = ab.replace("{{ site.email }}", SITE["email"])
    open(os.path.join(OUT, "about.html"), "w", encoding="utf-8").write(page("关于我", ab))

    # ---- posts ----
    for p in posts:
        tags = " · " + " / ".join(p["tags"]) if p["tags"] else ""
        body = f"""<article class="wrap post-page">
  <p class="eyebrow">{p['date'].replace('-', '.')}{tags}</p>
  <h1>{html.escape(p['title'])}</h1>
  <p class="post-excerpt">{html.escape(p['excerpt'])}</p>
  <div class="rule"></div>
  <div class="post-body">{markdown(p['body'])}</div>
  <p class="back-link"><a href="../index.html#writing">← 返回文章列表</a></p>
</article>"""
        open(os.path.join(OUT, "posts", p["slug"] + ".html"), "w", encoding="utf-8").write(
            page(p["title"], body, depth=1))

    # ---- css ----
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(W, "assets", "style.css"), encoding="utf-8") as s:
        css = s.read()
    open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8").write(css)

    for root, _, files in os.walk(OUT):
        for f in sorted(files):
            fp = os.path.join(root, f)
            print("  %-44s %d bytes" % (os.path.relpath(fp, OUT), os.path.getsize(fp)))


if __name__ == "__main__":
    main()
