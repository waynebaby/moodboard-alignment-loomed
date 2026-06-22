"""Shared constants and utility functions for moodboard-alignment scripts."""
from pathlib import Path

ARRAY_FIELDS = ["timeline", "frames", "slides", "states", "journey"]

NODE_LABELS = {
    "timeline": "方向节点",
    "frames": "视觉方案",
    "slides": "页面节点",
    "states": "互动状态",
    "journey": "用户旅程",
    "nodes": "方向节点",
}

PROJECT_NAMES = {
    "film": "影视/广告",
    "mv": "音乐 MV",
    "poster": "海报/美术",
    "brand": "品牌/产品",
    "ppt": "PPT/宣讲",
    "app": "网站/App",
    "game": "游戏/互动",
}

DIM_VISIBILITY = {
    "film":   {"emotion", "motion", "color", "composition", "style", "sound"},
    "mv":     {"emotion", "motion", "color", "composition", "style", "sound"},
    "poster": {"emotion", "color", "composition", "style"},
    "brand":  {"emotion", "color", "composition", "style"},
    "ppt":    {"emotion", "motion", "color", "composition", "style"},
    "app":    {"emotion", "motion", "color", "composition", "style"},
    "game":   {"emotion", "motion", "color", "composition", "style", "sound"},
}

DEFAULT_DIMS = {"emotion", "motion", "color", "composition", "style", "sound"}


def get_visible_dims(project_type: str = "", sound_enabled=None) -> set:
    """Return visible dimensions for a project type, with optional sound override.

    sound_enabled:
    - True: force show sound/audio for sound-led app/ppt/brand experiences.
    - False: force hide sound/audio.
    - None: use project-type default.
    """
    dims = set(DIM_VISIBILITY.get(project_type, DEFAULT_DIMS))
    if sound_enabled is True:
        dims.add("sound")
    elif sound_enabled is False:
        dims.discard("sound")
    return dims


def find_nodes(data: dict) -> tuple:
    """Find the node array in data.json. Returns (array_field_name, nodes_list)."""
    for key in ARRAY_FIELDS:
        if isinstance(data.get(key), list):
            return key, data[key]
    raise SystemExit("No node array found: expected timeline/frames/slides/states/journey")


def slug(s: str) -> str:
    """Convert a string to a filesystem-safe slug."""
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in "-_ ":
            out.append("-")
    val = "".join(out).strip("-")
    while "--" in val:
        val = val.replace("--", "-")
    return val or "node"


def as_list(v) -> list:
    """Normalize a value to a list."""
    if v in (None, "", [], {}):
        return []
    return v if isinstance(v, list) else [v]
