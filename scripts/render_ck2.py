#!/usr/bin/env python3
"""Render CK2 confirmation documents (client + execution)."""
import argparse
import html
import json
from pathlib import Path
from datetime import datetime

from utils import find_nodes, as_list, NODE_LABELS, PROJECT_NAMES, get_visible_dims


def esc(v):
    return html.escape(str(v if v is not None else ""))


def palette_html(palette):
    if not palette:
        return ""
    items = []
    for c in palette:
        if isinstance(c, dict):
            hx = c.get("hex", "#ccc")
            name = c.get("name", hx)
            usage = c.get("usage", "")
        else:
            hx, name, usage = str(c), str(c), ""
        items.append(f'<div class="swatch"><span style="background:{esc(hx)}"></span><b>{esc(name)}</b><small>{esc(hx)} {esc(usage)}</small></div>')
    return '<section class="card"><div class="section-kicker">Palette</div><h2>关键色板</h2><div class="palette">' + "".join(items) + "</div></section>"


def list_block(title, items, cls):
    vals = as_list(items)
    if not vals:
        return ""
    return f'<div class="summary-block {esc(cls)}"><b>{esc(title)}</b><ul>' + "".join(f"<li>{esc(x)}</li>" for x in vals) + "</ul></div>"


def node_meta(n, index, arr_name):
    bits = [f"{NODE_LABELS.get(arr_name, '时间节点')} {index:02d}"]
    for key in ["timeRange", "pageRange", "state", "screen", "variant"]:
        if n.get(key):
            bits.append(str(n.get(key)))
    return " · ".join(bits)


def render_node_client(n, index, arr_name):
    label = n.get("label", n.get("id", "node"))
    emo = n.get("emotion", {})
    emo_type = emo.get("type", "")
    kws = as_list(emo.get("keywords", []))
    time_range = n.get("timeRange", "")
    kw_parts = []
    if emo_type:
        kw_parts.append(f'<span class="node-kw-title">{esc(emo_type)}</span>')
    for k in kws:
        kw_parts.append(f'<span class="node-kw">{esc(k)}</span>')
    desc = n.get("image", {}).get("description", "") if isinstance(n.get("image"), dict) else ""
    if desc:
        kw_parts.append(f'<span class="node-desc">{esc(desc)}</span>')
    return f'''<section class="node card compact-node">
<div class="node-head"><h2>{esc(label)}</h2><div class="node-time">{esc(time_range)}</div></div>
<div class="node-kw-line">{" · ".join(kw_parts)}</div>
</section>'''


def render_node_execution(n, index, arr_name, ptype="", sound_enabled=None):
    label = n.get("label", n.get("id", "node"))
    meta = node_meta(n, index, arr_name)
    visible = get_visible_dims(ptype, sound_enabled)
    dim_order = [("emotion", "情绪"), ("motion", "动作/节奏"), ("color", "色彩"),
                 ("composition", "构图"), ("style", "风格/质感"), ("sound", "声音")]
    briefs = []
    for key, title in dim_order:
        if key not in visible:
            continue
        obj = n.get(key, {})
        if isinstance(obj, dict) and obj.get("description"):
            briefs.append(f"<p class='dim-brief'><b>{esc(title)}</b>：{esc(obj['description'])}</p>")
    return f'''<section class="node card">
<div class="node-head"><div class="node-meta">{esc(meta)}</div><h2>{esc(label)}</h2></div>
{''.join(briefs)}
</section>'''


def render(data, out_path, audience="client"):
    meta = data.get("meta", {})
    summary = data.get("summary", {})
    arr_name, nodes = find_nodes(data)
    project = meta.get("project", "Moodboard")
    ptype = meta.get("project_type", "")
    ptype_label = PROJECT_NAMES.get(ptype, ptype)
    style = meta.get("style", "")
    keywords = as_list(summary.get("keywords", []))
    one_sentence = summary.get("one_sentence", "")
    aligned = summary.get("aligned", [])
    risks = summary.get("risks", [])
    execution_notes = data.get("execution_notes", [])
    is_client = audience == "client"
    view_label = "Client · 客户确认版" if is_client else "Execution · 执行确认版"
    subtitle_note = "请确认整体方向和感觉是否正确" if is_client else "请确认创意方向和执行可行性"

    if is_client:
        node_html = "\n".join(render_node_client(n, i + 1, arr_name) for i, n in enumerate(nodes))
    else:
        node_html = "\n".join(render_node_execution(n, i + 1, arr_name, ptype, meta.get("sound_enabled")) for i, n in enumerate(nodes))

    notes_html = ""
    if not is_client and execution_notes:
        items = "".join(f"<li>{esc(x)}</li>" for x in execution_notes)
        notes_html = f'<section class="card"><div class="section-kicker">Execution Notes</div><h2>执行层注意</h2><ul class="exec-notes">{items}</ul></section>'

    if is_client:
        confirm_html = '''<section class="card confirm-box"><div class="section-kicker">请确认</div><h2>方向确认</h2><p>以上情绪方向是否正确？色彩倾向、整体调性、节奏安排是否符合预期？</p><p class="confirm-hint">如有调整，请在具体节点中标注修改意见。</p></section>'''
    else:
        confirm_html = '''<section class="card confirm-box"><div class="section-kicker">请确认</div><h2>执行可行性确认</h2><p>以上创意方向是否可以执行？预算、时间、技术、场地是否有约束？执行层注意中的要点是否有遗漏？</p><p class="confirm-hint">如有问题，请标注具体节点和需要调整的内容。</p></section>'''

    ts = datetime.now().strftime("%Y-%m-%d")
    ver = meta.get("version", 1)
    html_doc = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project)} · CK2 确认文档 · {esc(view_label)}</title>
<style>
:root{{--bg:#f6f2ea;--ink:#1f2328;--muted:#74706a;--card:#fffdf8;--line:#e4ded2;--accent:#9a6a3a;--soft:#f1e7d8;--tag-bg:rgba(255,255,255,.58);--card-bg:rgba(255,253,248,.88);--summary-bg:#faf5ec;--swatch-bg:#fff;--shadow:rgba(80,60,30,.06);--body-bg:radial-gradient(circle at 20% 0%,#fbf7ef 0,#f6f2ea 38%,#efe6d8 100%)}}
:root[data-theme="dark"]{{--bg:#12100e;--ink:#f2eadf;--muted:#b8aa9b;--card:#1f1a16;--line:#3b3028;--accent:#d9a66f;--soft:#2b241f;--tag-bg:rgba(217,166,111,.12);--card-bg:rgba(31,26,22,.9);--summary-bg:#251f1a;--swatch-bg:#211b17;--shadow:rgba(0,0,0,.32);--body-bg:radial-gradient(circle at 20% 0%,#2a211b 0,#15120f 42%,#0f0d0b 100%)}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--body-bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}}
header{{padding:64px 24px 34px;max-width:1120px;margin:auto;position:relative}} .theme-toggle{{position:fixed;right:18px;top:18px;z-index:20;border:1px solid var(--line);background:var(--card-bg);color:var(--ink);border-radius:999px;padding:8px 12px;font-size:13px;cursor:pointer;box-shadow:0 8px 24px var(--shadow);backdrop-filter:blur(8px)}} .theme-toggle:hover{{color:var(--accent)}} .kicker,.section-kicker{{text-transform:uppercase;letter-spacing:.14em;color:var(--accent);font-size:12px;font-weight:700;margin-bottom:8px}} h1{{font-size:46px;line-height:1.08;margin:0 0 12px;letter-spacing:-.03em}} .subtitle{{font-size:20px;color:var(--muted);max-width:820px}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}} .tag{{border:1px solid var(--line);background:var(--tag-bg);border-radius:999px;padding:5px 12px;color:var(--accent)}}
main{{max-width:1120px;margin:auto;padding:0 24px 56px}} .card{{background:var(--card-bg);border:1px solid var(--line);border-radius:24px;padding:24px;margin:18px 0;box-shadow:0 14px 38px var(--shadow);backdrop-filter:blur(8px)}}
.summary p{{font-size:23px;margin:0 0 14px}} .meta{{color:var(--muted);font-size:14px;margin-top:8px}} .summary-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:18px}} .summary-block{{background:var(--summary-bg);border:1px solid var(--line);border-radius:16px;padding:14px}} .summary-block ul{{margin:8px 0 0;padding-left:18px}}
.palette{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}} .swatch{{border:1px solid var(--line);border-radius:16px;padding:12px;background:var(--swatch-bg)}} .swatch span{{display:block;height:72px;border-radius:12px;margin-bottom:10px;border:1px solid rgba(0,0,0,.06)}} .swatch small{{display:block;color:var(--muted)}}
.node-meta{{font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:6px}} h2{{margin:0 0 14px;font-size:26px;letter-spacing:-.02em}}
.compact-node .node-head{{display:flex;align-items:baseline;gap:12px;margin-bottom:10px}} .compact-node h2{{margin:0}} .node-time{{color:var(--muted);font-size:14px}} .node-kw-line{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}} .node-kw-title{{font-weight:700;color:var(--ink)}} .node-kw{{background:var(--soft);border-radius:999px;padding:2px 10px;font-size:13px;color:var(--accent)}} .node-desc{{color:var(--muted);font-size:14px}}
.dim-brief{{margin:6px 0;color:var(--ink);font-size:15px}} .dim-brief b{{color:var(--accent)}}
.exec-notes{{margin:8px 0 0;padding-left:18px}} .exec-notes li{{margin:6px 0}}
.confirm-box{{background:var(--swatch-bg);border:2px solid var(--accent)}} .confirm-box h2{{color:var(--accent)}} .confirm-hint{{color:var(--muted);font-size:14px;margin-top:8px}}
footer{{max-width:1120px;margin:auto;padding:24px;color:var(--muted);font-size:13px}}
@media print{{:root,:root[data-theme="dark"]{{--bg:#fff;--ink:#1f2328;--muted:#74706a;--card:#fff;--line:#ddd;--accent:#9a6a3a;--soft:#f6f2ea;--tag-bg:#fff;--card-bg:#fff;--summary-bg:#fff;--swatch-bg:#fff;--shadow:transparent;--body-bg:#fff}}body{{background:#fff}}.theme-toggle{{display:none}}.card{{box-shadow:none;border:1px solid #ddd;break-inside:avoid}}header{{padding-top:32px}}}}
@media(max-width:760px){{header{{padding-top:44px}}h1{{font-size:34px}}.summary-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<button class="theme-toggle" type="button" aria-label="切换亮暗主题">🌙 暗色</button>
<header>
  <div class="kicker">CK2 · {esc(view_label)}</div>
  <h1>{esc(project)}</h1>
  <div class="subtitle">{esc(style)}</div>
  <div class="tags">{''.join(f'<span class="tag">{esc(k)}</span>' for k in keywords)}</div>
</header>
<main>
<section class="card summary">
  <div class="section-kicker">Direction Summary</div>
  <p>{esc(one_sentence)}</p>
  <div class="meta">项目类型：{esc(ptype_label)} · 文档版本：v{esc(ver)} · 日期：{esc(ts)} · {esc(subtitle_note)}</div>
  <div class="summary-grid">
    {list_block('已对齐共识', aligned, 'aligned')}
    {'' if is_client else list_block('风险提醒', risks, 'risks')}
  </div>
</section>
{palette_html(data.get('palette', []))}
<section class="section-head"><div class="section-kicker">Direction Nodes</div></section>
{node_html}
{notes_html}
{confirm_html}
</main>
<footer>Generated by moodboard-alignment skill · CK2 {esc(audience)} · {esc(datetime.now().isoformat(timespec='seconds'))}</footer>
<script>
(function(){{
  var root=document.documentElement;
  var btn=document.querySelector('.theme-toggle');
  var key='moodboard-theme';
  function apply(theme){{
    root.setAttribute('data-theme', theme);
    if(btn) btn.textContent = theme === 'dark' ? '☀️ 亮色' : '🌙 暗色';
  }}
  var saved=localStorage.getItem(key) || 'light';
  apply(saved);
  if(btn) btn.addEventListener('click', function(){{
    var next=root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    localStorage.setItem(key,next);
    apply(next);
  }});
}})();
</script>
</body>
</html>'''
    out_path.write_text(html_doc, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Render CK2 confirmation documents")
    ap.add_argument("--data-json", required=True, help="Path to data.json")
    ap.add_argument("--output", required=True, help="Output HTML path")
    ap.add_argument("--audience", required=True, choices=["client", "execution"], help="Target audience")
    args = ap.parse_args()
    data_path = Path(args.data_json)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    render(data, out_path, audience=args.audience)
    print(str(out_path))


if __name__ == "__main__":
    main()
