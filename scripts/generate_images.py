#!/usr/bin/env python3
"""Generate node direction images via Agnes image API."""
import argparse
import base64
import json
import os
import urllib.request
from pathlib import Path
from datetime import datetime

from utils import find_nodes, slug
from config import DEFAULT_IMAGE_MODEL, IMAGE_SIZES, IMAGE_BASE_URL, IMAGE_API_KEY


def _request_json(url, payload, api_key, timeout=300):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download_url(url, output_path, timeout=300):
    req = urllib.request.Request(url, headers={"User-Agent": "moodboard-alignment/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        output_path.write_bytes(resp.read())


def generate_image(prompt, output_path, api_key, base_url, model=DEFAULT_IMAGE_MODEL, size="1024x1024"):
    """Call OpenAI-compatible /images/generations and write one image file."""
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": "standard",
        "n": 1,
    }
    result = _request_json(f"{base_url.rstrip('/')}/images/generations", payload, api_key)
    data = result.get("data") or []
    if not data:
        raise RuntimeError(f"No image data returned: {json.dumps(result, ensure_ascii=False)[:300]}")

    item = data[0]
    if item.get("b64_json"):
        output_path.write_bytes(base64.b64decode(item["b64_json"]))
        return "b64_json"
    if item.get("url"):
        _download_url(item["url"], output_path)
        return "url"

    # Be tolerant of provider-specific response keys.
    for key in ("image", "data", "base64"):
        val = item.get(key)
        if isinstance(val, str) and len(val) > 100:
            output_path.write_bytes(base64.b64decode(val.split(",")[-1]))
            return key

    raise RuntimeError(f"Unsupported image response: {json.dumps(item, ensure_ascii=False)[:300]}")


def main():
    ap = argparse.ArgumentParser(description="Generate direction images for moodboard nodes")
    ap.add_argument("--data-json", required=True, help="Path to data.json")
    ap.add_argument("--output-dir", default=None, help="Image output directory (default: <project>/images)")
    ap.add_argument("--model", default=DEFAULT_IMAGE_MODEL, help=f"Image model (default: {DEFAULT_IMAGE_MODEL})")
    ap.add_argument("--base-url", default=None, help=f"Image API base URL (default: IMAGE_BASE_URL env or {IMAGE_BASE_URL})")
    ap.add_argument("--node-id", default=None, help="Only generate for one node id")
    ap.add_argument("--size", default=None, help="Override image size (e.g. 1024x1024)")
    args = ap.parse_args()

    api_key = IMAGE_API_KEY
    if not api_key:
        raise SystemExit("IMAGE_API_KEY not set. If using Agnes, set AGNES_API_KEY instead.")
    base_url = args.base_url or IMAGE_BASE_URL

    data_path = Path(args.data_json)
    project_dir = data_path.parent
    out_dir = Path(args.output_dir) if args.output_dir else project_dir / "images"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    _, nodes = find_nodes(data)
    aspect = data.get("meta", {}).get("aspectRatio", "1:1")
    size = args.size or IMAGE_SIZES.get(aspect, "1024x1024")
    generated = []

    for node in nodes:
        if args.node_id and node.get("id") != args.node_id:
            continue
        prompt = node.get("image_prompt") or node.get("image", {}).get("description") or node.get("label")
        if not prompt:
            continue

        print(f"Generating {node.get('id')} with {args.model}...", flush=True)
        node_id = slug(node.get("id") or node.get("label") or "node")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = out_dir / f"{node_id}_{stamp}.png"
        image = node.setdefault("image", {})

        try:
            source_type = generate_image(prompt, dest, api_key, base_url, model=args.model, size=size)
            rel = dest.relative_to(project_dir) if dest.is_relative_to(project_dir) else dest
            image["url"] = str(rel)
            image["status"] = "generated"
            image["model"] = args.model
            image["size"] = size
            image["source_type"] = source_type
            image["generated_at"] = datetime.now().isoformat(timespec="seconds")
            image.pop("error", None)
            generated.append(str(dest))
            print(f"  OK: {dest}")
        except Exception as e:
            image.setdefault("url", "")
            image["status"] = "placeholder"
            image["error"] = str(e)[:500]
            print(f"  FAILED: {node.get('id')}: {e}", flush=True)

    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"generated": generated, "data_json": str(data_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
