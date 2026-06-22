#!/usr/bin/env python3
"""Render moodboard HTML views from data.json."""
import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
from datetime import datetime

from utils import find_nodes, slug, as_list, NODE_LABELS, PROJECT_NAMES, get_visible_dims


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


def value_to_text(v):
    if isinstance(v, list):
        return " / ".join(map(str, v))
    if isinstance(v, dict):
        return "；".join(f"{k}: {value_to_text(val)}" for k, val in v.items() if val not in (None, "", [], {}))
    return str(v)


def dim(title, obj):
    if not isinstance(obj, dict):
        return ""
    order = ["type", "intensity", "keywords", "palette", "temperature", "saturation", "camera", "dof", "density", "reverb", "texture", "reference", "description"]
    keys = [k for k in order if k in obj] + [k for k in obj.keys() if k not in order]
    bits = []
    for k in keys:
        v = obj.get(k)
        if v in (None, "", [], {}):
            continue
        bits.append(f"<li><b>{esc(k)}</b>：{esc(value_to_text(v))}</li>")
    if not bits:
        return ""
    return f"<details open><summary>{esc(title)}</summary><ul>{''.join(bits)}</ul></details>"


def placeholder_svg(label, color="#ddd"):
    safe = esc(label)
    return f'''<div class="placeholder" style="background:linear-gradient(135deg,{esc(color)},#f7f4ee)"><div>{safe}</div><small>mood image</small></div>'''


def node_meta(n, index, arr_name):
    bits = [f"{NODE_LABELS.get(arr_name, '方向节点')} {index:02d}"]
    for key in ["timeRange", "pageRange", "state", "screen", "variant"]:
        if n.get(key):
            bits.append(str(n.get(key)))
    return " · ".join(bits)


def to_data_uri(path, base_dir):
    full = (base_dir / path).resolve()
    if not full.exists():
        return None
    mime, _ = mimetypes.guess_type(str(full))
    if not mime:
        mime = "application/octet-stream"
    raw = full.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def get_image_html(n, base_dir=None, embed=False):
    label = n.get("label", n.get("id", "node"))
    img = n.get("image", {}) if isinstance(n.get("image"), dict) else {}
    url = img.get("url", "")
    if url:
        src = url
        if embed and base_dir:
            data_uri = to_data_uri(url, base_dir)
            if data_uri:
                src = data_uri
        safe_src = esc(src)
        safe_label = esc(label)
        return f'<button class="image-open" type="button" data-full="{safe_src}" data-title="{safe_label}" aria-label="查看原比例图片：{safe_label}"><img src="{safe_src}" alt="{safe_label}"><span class="image-open-hint">点击查看原比例</span></button>'
    pal = n.get("color", {}).get("palette", []) if isinstance(n.get("color"), dict) else []
    color = pal[0] if pal else "#d8d2c8"
    return placeholder_svg(label, color)


def get_audio_html(n, base_dir=None, embed=False):
    audio = n.get("audio", {})
    if not isinstance(audio, dict) or not audio.get("url"):
        return ""
    url = audio["url"]
    if embed and base_dir:
        data_uri = to_data_uri(url, base_dir)
        if data_uri:
            return f'<div class="audio-ref"><div class="section-kicker">Sound Reference</div><audio controls preload="none" src="{esc(data_uri)}"></audio></div>'
    return f'<div class="audio-ref"><div class="section-kicker">Sound Reference</div><audio controls preload="none" src="{esc(url)}"></audio></div>'


def node_keywords_line(n):
    emo = n.get("emotion", {})
    kws = as_list(emo.get("keywords", []))
    emo_type = emo.get("type", "")
    desc = n.get("image", {}).get("description", "") if isinstance(n.get("image"), dict) else ""
    parts = []
    if emo_type:
        parts.append(f'<span class="node-kw-title">{esc(emo_type)}</span>')
    for k in kws:
        parts.append(f'<span class="node-kw">{esc(k)}</span>')
    if desc:
        parts.append(f'<span class="node-desc">{esc(desc)}</span>')
    return " · ".join(parts)


# ── Node renderers ──────────────────────────────────────────────

def render_node_client(n, index, arr_name, ptype="", base_dir=None, embed=False, sound_enabled=None):
    label = n.get("label", n.get("id", "node"))
    image_html = get_image_html(n, base_dir, embed)
    kw_line = node_keywords_line(n)
    visible = get_visible_dims(ptype, sound_enabled)
    audio_html = get_audio_html(n, base_dir, embed) if "sound" in visible else ""
    return f'''<section class="node card client-node">
<div class="node-img client-img">{image_html}</div>
<div class="node-body"><h2>{esc(label)}</h2><div class="node-kw-line">{kw_line}</div>{audio_html}</div>
</section>'''


def render_node_director(n, index, arr_name, ptype="", base_dir=None, embed=False, sound_enabled=None):
    label = n.get("label", n.get("id", "node"))
    image_html = get_image_html(n, base_dir, embed)
    visible = get_visible_dims(ptype, sound_enabled)
    dim_order = ["emotion", "motion", "color", "composition", "style", "sound"]
    briefs = []
    for key in dim_order:
        if key not in visible:
            continue
        obj = n.get(key, {})
        if isinstance(obj, dict) and obj.get("description"):
            briefs.append(f"<p class='dim-brief'><b>{esc(key.capitalize())}</b>：{esc(obj['description'])}</p>")
    audio_html = get_audio_html(n, base_dir, embed) if "sound" in visible else ""
    return f'''<section class="node card">
<div class="node-img">{image_html}</div>
<div class="node-body"><div class="node-meta">{esc(node_meta(n, index, arr_name))}</div><h2>{esc(label)}</h2>{''.join(briefs)}{audio_html}</div>
</section>'''


def render_node_execution(n, index, arr_name, ptype="", base_dir=None, embed=False, sound_enabled=None):
    label = n.get("label", n.get("id", "node"))
    image_html = get_image_html(n, base_dir, embed)
    visible = get_visible_dims(ptype, sound_enabled)
    all_dims = [
        ("emotion",     "情绪 Emotion",      n.get("emotion", {})),
        ("motion",      "动作/节奏 Motion",   n.get("motion", {})),
        ("color",       "色彩 Color",         n.get("color", {})),
        ("composition", "构图 Composition",    n.get("composition", {})),
        ("style",       "风格/质感 Style",     n.get("style", {})),
        ("sound",       "声音 Sound",         n.get("sound", {})),
    ]
    parts = [dim(title, obj) for key, title, obj in all_dims if key in visible and obj not in (None, "", {}, [])]
    prompt = n.get("image_prompt", "")
    if prompt:
        parts.append(f'<details><summary>Image Prompt</summary><p class="prompt">{esc(prompt)}</p></details>')
    audio_html = get_audio_html(n, base_dir, embed) if "sound" in visible else ""
    return f'''<section class="node card">
<div class="node-img">{image_html}</div>
<div class="node-body"><div class="node-meta">{esc(node_meta(n, index, arr_name))}</div><h2>{esc(label)}</h2>{''.join(parts)}{audio_html}</div>
</section>'''


NODE_RENDERERS = {
    "client": render_node_client,
    "director": render_node_director,
    "execution": render_node_execution,
}

# ── Main render ─────────────────────────────────────────────────

VIEW_LABELS = {
    "client": "Client · 甲方确认版",
    "director": "Director · 汇报版",
    "execution": "Execution · 执行完整版",
}


def list_block(title, items, cls):
    vals = as_list(items)
    if not vals:
        return ""
    return f'<div class="summary-block {esc(cls)}"><b>{esc(title)}</b><ul>' + "".join(f"<li>{esc(x)}</li>" for x in vals) + "</ul></div>"


def execution_notes_html(notes, view):
    vals = as_list(notes)
    if view == "client" or not vals:
        return ""
    items = "".join(f"<li>{esc(x)}</li>" for x in vals)
    return f'<section class="card"><div class="section-kicker">Execution Notes</div><h2>执行层注意</h2><ul class="exec-notes">{items}</ul></section>'


def render(data, out_path, view=None, embed=False):
    meta = data.get("meta", {})
    summary = data.get("summary", {})
    arr_name, nodes = find_nodes(data)
    project = meta.get("project", "Moodboard")
    ptype = meta.get("project_type", "")
    ptype_label = PROJECT_NAMES.get(ptype, ptype)
    style = meta.get("style", "")
    keywords = as_list(summary.get("keywords", []))
    view = view or data.get("view", "execution")
    if view not in NODE_RENDERERS:
        view = "execution"
    render_fn = NODE_RENDERERS[view]
    base_dir = out_path.parent
    sound_enabled = meta.get("sound_enabled")
    node_html = "\n".join(render_fn(n, i + 1, arr_name, ptype, base_dir, embed, sound_enabled) for i, n in enumerate(nodes))
    data_json = json.dumps(data, ensure_ascii=False)
    summary_grid = ""
    if view != "client":
        summary_grid = f'''<div class="summary-grid">
    {list_block('已对齐共识', summary.get('aligned', []), 'aligned')}
    {list_block('风险提醒', summary.get('risks', []), 'risks')}
  </div>'''
    view_label = VIEW_LABELS
    html_doc = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project)} · 情绪板 · {esc(view_label.get(view, view))}</title>
<style>
:root{{--bg:#f6f2ea;--ink:#1f2328;--muted:#74706a;--card:#fffdf8;--line:#e4ded2;--accent:#9a6a3a;--soft:#f1e7d8;--tag-bg:rgba(255,255,255,.58);--card-bg:rgba(255,253,248,.88);--summary-bg:#faf5ec;--swatch-bg:#fff;--shadow:rgba(80,60,30,.06);--body-bg:radial-gradient(circle at 20% 0%,#fbf7ef 0,#f6f2ea 38%,#efe6d8 100%)}}
:root[data-theme="dark"]{{--bg:#12100e;--ink:#f2eadf;--muted:#b8aa9b;--card:#1f1a16;--line:#3b3028;--accent:#d9a66f;--soft:#2b241f;--tag-bg:rgba(217,166,111,.12);--card-bg:rgba(31,26,22,.9);--summary-bg:#251f1a;--swatch-bg:#211b17;--shadow:rgba(0,0,0,.32);--body-bg:radial-gradient(circle at 20% 0%,#2a211b 0,#15120f 42%,#0f0d0b 100%)}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--body-bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65}}
header{{padding:64px 24px 34px;max-width:1120px;margin:auto;position:relative}} .theme-toggle{{position:fixed;right:18px;top:18px;z-index:20;border:1px solid var(--line);background:var(--card-bg);color:var(--ink);border-radius:999px;padding:8px 12px;font-size:13px;cursor:pointer;box-shadow:0 8px 24px var(--shadow);backdrop-filter:blur(8px)}} .theme-toggle:hover{{color:var(--accent)}} .kicker,.section-kicker{{text-transform:uppercase;letter-spacing:.14em;color:var(--accent);font-size:12px;font-weight:700;margin-bottom:8px}} h1{{font-size:46px;line-height:1.08;margin:0 0 12px;letter-spacing:-.03em}} .subtitle{{font-size:20px;color:var(--muted);max-width:820px}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}} .tag{{border:1px solid var(--line);background:var(--tag-bg);border-radius:999px;padding:5px 12px;color:var(--accent)}}
main{{max-width:1120px;margin:auto;padding:0 24px 56px}} .card{{background:var(--card-bg);border:1px solid var(--line);border-radius:24px;padding:24px;margin:18px 0;box-shadow:0 14px 38px var(--shadow);backdrop-filter:blur(8px)}}
.summary p{{font-size:23px;margin:0 0 14px}} .meta{{color:var(--muted);font-size:14px;margin-top:8px}} .summary-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:18px}} .summary-block{{background:var(--summary-bg);border:1px solid var(--line);border-radius:16px;padding:14px}} .summary-block ul{{margin:8px 0 0;padding-left:18px}}
.palette{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}} .swatch{{border:1px solid var(--line);border-radius:16px;padding:12px;background:var(--swatch-bg)}} .swatch span{{display:block;height:72px;border-radius:12px;margin-bottom:10px;border:1px solid rgba(0,0,0,.06)}} .swatch small{{display:block;color:var(--muted)}}
.node{{display:grid;grid-template-columns:minmax(280px,42%) 1fr;gap:24px;align-items:start}} .node-img{{position:sticky;top:18px}} .node-img img,.placeholder{{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:20px;border:1px solid var(--line);display:block}}
.image-open{{position:relative;width:100%;padding:0;border:0;background:transparent;display:block;cursor:zoom-in;color:inherit;text-align:inherit}} .image-open img{{transition:transform .22s ease,filter .22s ease}} .image-open:hover img{{transform:scale(1.012);filter:saturate(1.03)}} .image-open-hint{{position:absolute;right:10px;bottom:10px;background:rgba(0,0,0,.55);color:#fff;border-radius:999px;padding:4px 9px;font-size:12px;opacity:0;transition:opacity .18s ease;pointer-events:none}} .image-open:hover .image-open-hint{{opacity:1}}
.placeholder{{display:grid;place-items:center;text-align:center;color:var(--ink);font-size:28px;font-weight:700}} .placeholder small{{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.55}}
.node-meta{{font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:6px}} h2{{margin:0 0 14px;font-size:26px;letter-spacing:-.02em}} details{{border-top:1px solid var(--line);padding:10px 0}} summary{{cursor:pointer;font-weight:750;color:var(--ink)}} ul{{margin:8px 0 0;padding-left:18px}} .prompt{{background:var(--soft);border-radius:12px;padding:12px;color:var(--ink)}}
.dim-brief{{margin:6px 0;color:var(--ink);font-size:15px}} .dim-brief b{{color:var(--accent)}}
.audio-ref{{margin:14px 0 4px;padding:12px;background:var(--soft);border-radius:12px}} .audio-ref audio{{width:100%;margin-top:8px;height:40px}}
.exec-notes{{margin:8px 0 0;padding-left:18px}} .exec-notes li{{margin:6px 0}}
.node-kw-line{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:4px}} .node-kw-title{{font-weight:700;color:var(--ink)}} .node-kw{{background:var(--soft);border-radius:999px;padding:2px 10px;font-size:13px;color:var(--accent)}} .node-desc{{color:var(--muted);font-size:14px}}
footer{{max-width:1120px;margin:auto;padding:24px;color:var(--muted);font-size:13px}}
.lightbox{{position:fixed;inset:0;z-index:60;background:rgba(12,10,8,.86);display:none;align-items:center;justify-content:center;padding:34px;backdrop-filter:blur(10px)}} .lightbox.open{{display:flex}} .lightbox img{{max-width:min(96vw,1600px);max-height:88vh;width:auto;height:auto;object-fit:contain;border-radius:18px;box-shadow:0 24px 80px rgba(0,0,0,.45);background:#111}} .lightbox-title{{position:absolute;left:28px;bottom:20px;color:#f7f3ed;font-size:14px;opacity:.86}} .lightbox-close{{position:absolute;right:24px;top:20px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.1);color:#fff;border-radius:999px;padding:8px 12px;cursor:pointer;font-size:14px}} .lightbox-close:hover{{background:rgba(255,255,255,.18)}}
@media print{{:root,:root[data-theme="dark"]{{--bg:#fff;--ink:#1f2328;--muted:#74706a;--card:#fff;--line:#ddd;--accent:#9a6a3a;--soft:#f6f2ea;--tag-bg:#fff;--card-bg:#fff;--summary-bg:#fff;--swatch-bg:#fff;--shadow:transparent;--body-bg:#fff}}body{{background:#fff}}.theme-toggle,.lightbox,.image-open-hint{{display:none}}.card{{box-shadow:none;border:1px solid #ddd;break-inside:avoid}}header{{padding-top:32px}}}}
@media(max-width:760px){{header{{padding-top:44px}}h1{{font-size:34px}}.summary-grid{{grid-template-columns:1fr}}.node{{grid-template-columns:1fr}}.node-img{{position:relative;top:auto}}}}
</style>
</head>
<body>
<button class="theme-toggle" type="button" aria-label="切换亮暗主题">🌙 暗色</button>
<header>
  <div class="kicker">Moodboard · {esc(view_label.get(view, view))}</div>
  <h1>{esc(project)}</h1>
  <div class="subtitle">{esc(style)}</div>
  <div class="tags">{''.join(f'<span class="tag">{esc(k)}</span>' for k in keywords)}</div>
</header>
<main>
<section class="card summary">
  <div class="section-kicker">Direction Summary</div>
  <p>{esc(summary.get('one_sentence',''))}</p>
  {f'<div class="meta">项目类型：{esc(ptype_label)} · 视图：{esc(view_label.get(view, view))} · 版本：v{esc(meta.get("version",1))}</div>' if view != 'client' else ''}
  {summary_grid}
</section>
{palette_html(data.get('palette', []))}
<section class="section-head"><div class="section-kicker">Direction Nodes</div></section>
{node_html}
{execution_notes_html(data.get('execution_notes', []), view)}
</main>
<div class="lightbox" aria-hidden="true">
  <button class="lightbox-close" type="button">关闭 Esc</button>
  <img alt="">
  <div class="lightbox-title"></div>
</div>
<footer>Generated by moodboard-alignment skill · {esc(view)} view · {esc(datetime.now().isoformat(timespec='seconds'))}</footer>
<script id="moodboard-data" type="application/json">{esc(data_json)}</script>
<script>
(function(){{
  var box=document.querySelector('.lightbox');
  if(!box) return;
  var img=box.querySelector('img');
  var title=box.querySelector('.lightbox-title');
  var close=box.querySelector('.lightbox-close');
  function open(src,label){{
    img.src=src;
    img.alt=label || '';
    title.textContent=label || '原比例图片';
    box.classList.add('open');
    box.setAttribute('aria-hidden','false');
  }}
  function hide(){{
    box.classList.remove('open');
    box.setAttribute('aria-hidden','true');
    img.removeAttribute('src');
  }}
  document.querySelectorAll('.image-open').forEach(function(btn){{
    btn.addEventListener('click', function(){{ open(btn.dataset.full, btn.dataset.title); }});
  }});
  if(close) close.addEventListener('click', hide);
  box.addEventListener('click', function(e){{ if(e.target === box) hide(); }});
  document.addEventListener('keydown', function(e){{ if(e.key === 'Escape') hide(); }});
}})();
</script>
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
    ap = argparse.ArgumentParser(description="Render moodboard HTML views")
    ap.add_argument("--data-json", required=True, help="Path to data.json")
    ap.add_argument("--output", required=True, help="Output HTML path")
    ap.add_argument("--view", default=None, choices=["client", "director", "execution"], help="View to render")
    ap.add_argument("--embed", action="store_true", help="Embed images/audio as base64 (self-contained HTML)")
    args = ap.parse_args()
    data_path = Path(args.data_json)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    render(data, out_path, view=args.view, embed=args.embed)
    print(str(out_path))


if __name__ == "__main__":
    main()
