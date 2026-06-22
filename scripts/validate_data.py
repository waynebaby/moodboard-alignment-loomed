#!/usr/bin/env python3
"""Validate moodboard data.json structure and referenced assets."""
import argparse
import json
import sys
from pathlib import Path

from utils import ARRAY_FIELDS, DEFAULT_DIMS, find_nodes, get_visible_dims
from config import IMAGE_SIZES

VALID_PROJECT_TYPES = {"film", "poster", "ppt", "game", "app", "mv", "brand"}
REQUIRED_TOP = ["meta", "summary", "palette"]
REQUIRED_NODE = ["id", "label", "emotion", "motion", "color", "composition", "style", "sound", "image", "image_prompt"]


def is_bool_or_none(v):
    return v is None or isinstance(v, bool)


def check_file(base_dir, rel_path):
    if not rel_path or str(rel_path).startswith(("http://", "https://", "data:")):
        return True
    return (base_dir / rel_path).exists()


def main():
    ap = argparse.ArgumentParser(description="Validate moodboard data.json")
    ap.add_argument("--data-json", required=True, help="Path to data.json")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors")
    args = ap.parse_args()

    data_path = Path(args.data_json)
    base_dir = data_path.parent
    errors = []
    warnings = []

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: cannot read JSON: {e}")
        return 2

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"Missing top-level field: {key}")

    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    ptype = meta.get("project_type", "")
    if ptype and ptype not in VALID_PROJECT_TYPES:
        warnings.append(f"Unknown project_type: {ptype}; default dimensions will be used")
    if meta.get("aspectRatio") and meta.get("aspectRatio") not in IMAGE_SIZES:
        warnings.append(f"Unsupported aspectRatio: {meta.get('aspectRatio')}; image generation will fall back to 1024x1024")
    if not is_bool_or_none(meta.get("sound_enabled")):
        warnings.append("meta.sound_enabled should be true/false when present")

    arrays = [k for k in ARRAY_FIELDS if isinstance(data.get(k), list)]
    if not arrays:
        errors.append("No node array found: expected one of timeline/frames/slides/states/journey")
        nodes = []
        arr_name = ""
    else:
        if len(arrays) > 1:
            warnings.append(f"Multiple node arrays found {arrays}; renderer will use {arrays[0]}")
        arr_name, nodes = find_nodes(data)
        expected = {
            "film": "timeline", "mv": "timeline", "poster": "frames", "brand": "frames",
            "ppt": "slides", "game": "states", "app": "journey",
        }.get(ptype)
        if expected and arr_name != expected:
            warnings.append(f"project_type={ptype} usually uses '{expected}', but found '{arr_name}'")

    visible = get_visible_dims(ptype, meta.get("sound_enabled"))

    for i, node in enumerate(nodes, 1):
        if not isinstance(node, dict):
            errors.append(f"Node {i} is not an object")
            continue
        node_id = node.get("id") or f"#{i}"
        for key in REQUIRED_NODE:
            if key not in node:
                warnings.append(f"Node {node_id}: missing field '{key}'")
        if node.get("id") and any(ch for ch in str(node.get("id")) if not (ch.islower() or ch.isdigit() or ch == "-")):
            warnings.append(f"Node {node_id}: id should use lowercase letters, numbers, and hyphens only")
        for dim in DEFAULT_DIMS:
            if dim in node and not isinstance(node.get(dim), dict):
                warnings.append(f"Node {node_id}: '{dim}' should be an object")
        image = node.get("image", {})
        if not isinstance(image, dict):
            warnings.append(f"Node {node_id}: image should be an object")
        else:
            url = image.get("url", "")
            if url and not check_file(base_dir, url):
                warnings.append(f"Node {node_id}: image file not found: {url}")
        audio = node.get("audio", {})
        if audio not in ({}, None) and not isinstance(audio, dict):
            warnings.append(f"Node {node_id}: audio should be an object")
        elif isinstance(audio, dict):
            url = audio.get("url", "")
            if url and not check_file(base_dir, url):
                warnings.append(f"Node {node_id}: audio file not found: {url}")
            if url and "sound" not in visible:
                warnings.append(f"Node {node_id}: audio exists but sound is hidden for this project_type unless meta.sound_enabled=true")
        if not node.get("image_prompt"):
            warnings.append(f"Node {node_id}: image_prompt is empty; image generation will use fallback description/label")

    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARN: {msg}")
    print(json.dumps({"errors": len(errors), "warnings": len(warnings), "data_json": str(data_path)}, ensure_ascii=False))

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
