"""
解析 ai-news-YYYYMMDD-HHMM.html 并以 markdown 格式推送到企微「ai新闻」群机器人。

HTML 结构假设：
- <title>AI Daily · {DISPLAY_DATE}</title>
- <div id="panel-ai">…10 条 <article class="card"> 每条含 <span class="card-tag">emoji 中文</span>、<h2 class="card-title">标题</h2>、<p class="card-summary">摘要</p>
- <div id="panel-market">…5 条同上格式

WEBHOOK_URL 通过环境变量传入。
"""

import os
import re
import sys
import json
import urllib.request


SUMMARY_MAX_CHARS = 32  # 企微 markdown.content 硬上限 4096 字节；15 条 × ~32 字摘要 + 标题 + 标签，留 ~200 字节安全边距


def extract_panels(html: str):
    """切出 panel-ai / panel-market 两段 HTML 子串。"""
    parts = re.split(r'<div id="panel-(\w+)"', html)
    panels = {}
    # parts[0] = 文件头到第一个 panel；后面成对：name, body
    for i in range(1, len(parts), 2):
        name = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        panels[name] = body
    return panels


CARD_PATTERN = re.compile(
    r'<span class="card-tag">(.+?)</span>'  # group 1: tag like "💰 商业融资"
    r'.*?'
    r'<h2 class="card-title">(.+?)</h2>'    # group 2: title
    r'\s*<p class="card-summary">(.+?)</p>',  # group 3: summary
    re.DOTALL,
)


def parse_cards(panel_html: str):
    """返回 [{"emoji", "title", "summary"}, ...]，emoji 取 card-tag 第一个字符。"""
    items = []
    for tag, title, summary in CARD_PATTERN.findall(panel_html):
        # tag 形如 "💰 商业融资"，取首字符
        emoji = tag.strip()[0] if tag.strip() else ""
        items.append({
            "emoji": emoji,
            "title": _clean(title),
            "summary": _clean(summary),
        })
    return items


def _clean(text: str) -> str:
    """去 HTML 标签、转义、压缩空白。"""
    text = re.sub(r'<[^>]+>', '', text)
    text = (text.replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&quot;", '"')
                .replace("&#39;", "'"))
    return re.sub(r'\s+', ' ', text).strip()


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 1] + "…"


def extract_display_date(html: str) -> str:
    m = re.search(r'<title>\s*AI Daily\s*[·\.]?\s*(.+?)\s*</title>', html)
    return m.group(1).strip() if m else ""


def build_wechat_markdown(display_date: str, ai_items: list, market_items: list, page_url: str) -> str:
    def line_pair(num: int, emoji: str, title: str, summary: str, is_headline: bool = False) -> str:
        color = "warning" if is_headline else "info"
        show_emoji = "🔥" if is_headline else emoji
        return (
            f'<font color="{color}">{num:02d} {show_emoji}</font> **{title}**\n'
            f'<font color="comment">▸ {truncate(summary, SUMMARY_MAX_CHARS)}</font>'
        )

    ai_lines = [
        line_pair(i + 1, it["emoji"], it["title"], it["summary"], is_headline=(i == 0))
        for i, it in enumerate(ai_items)
    ]
    market_lines = [
        line_pair(i + 1, it["emoji"], it["title"], it["summary"], is_headline=False)
        for i, it in enumerate(market_items)
    ]

    content = (
        f'🗒️ **AI 日报 · {display_date}**\n'
        f'<font color="comment">精选 {len(ai_items)} 条 AI 快讯 + {len(market_items)} 条市场动态</font>\n\n'
        f'**🤖 AI 快讯**\n' + "\n".join(ai_lines) + "\n\n"
        f'**📈 市场动态**\n' + "\n".join(market_lines) + "\n\n"
        f'[📰 阅读完整版]({page_url})'
    )
    return content


def post_to_wechat(webhook_url: str, content: str) -> dict:
    payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {"content": content},
    }).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def main():
    if len(sys.argv) < 2:
        print("Usage: send_to_wechat.py <path/to/ai-news-YYYYMMDD-HHMM.html>", file=sys.stderr)
        sys.exit(2)

    html_path = sys.argv[1]
    webhook = os.environ.get("WEBHOOK_URL", "").strip()
    if not webhook:
        print("❌ WEBHOOK_URL 未设置（应来自 Actions Secret WECHAT_WEBHOOK_AINEWS）", file=sys.stderr)
        sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    display_date = extract_display_date(html)
    panels = extract_panels(html)
    ai_items = parse_cards(panels.get("ai", ""))
    market_items = parse_cards(panels.get("market", ""))

    if not ai_items or not market_items:
        print(f"❌ 解析失败：AI 条目 {len(ai_items)}、市场条目 {len(market_items)}", file=sys.stderr)
        sys.exit(1)

    filename = os.path.basename(html_path)
    page_url = f"https://yang-builds.github.io/ai-news/{filename}"

    wechat_md = build_wechat_markdown(display_date, ai_items, market_items, page_url)
    result = post_to_wechat(webhook, wechat_md)

    if result.get("errcode") == 0:
        print(f"✅ 推送成功 | {display_date} | AI {len(ai_items)} + 市场 {len(market_items)}")
    else:
        print(f"❌ 推送失败 | {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
