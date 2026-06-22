#!/usr/bin/env python3
"""Generate node sound references via Mimo TTS API."""
import argparse
import base64
import json
import urllib.request
from pathlib import Path
from datetime import datetime

from utils import find_nodes, slug
from config import DEFAULT_AUDIO_MODEL, AUDIO_BASE_URL, AUDIO_API_KEY, AUDIO_PROVIDER


def generate_audio(voice_prompt, text, output_path, api_key, base_url, model=DEFAULT_AUDIO_MODEL, fmt="wav"):
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": voice_prompt},
            {"role": "assistant", "content": text},
        ],
        "audio": {"format": fmt},
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"api-key": api_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    msg = result.get("choices", [{}])[0].get("message", {})
    audio_data = msg.get("audio", {})
    if not audio_data or not audio_data.get("data"):
        raise RuntimeError(f"No audio data returned: {json.dumps(result, ensure_ascii=False)[:200]}")
    audio_bytes = base64.b64decode(audio_data["data"])
    output_path.write_bytes(audio_bytes)
    return len(audio_bytes)


def main():
    ap = argparse.ArgumentParser(description="Generate sound reference audio for moodboard nodes")
    ap.add_argument("--data-json", required=True, help="Path to data.json")
    ap.add_argument("--output-dir", default=None, help="Audio output directory (default: <project>/audio)")
    ap.add_argument("--model", default=DEFAULT_AUDIO_MODEL, help=f"TTS model (default: {DEFAULT_AUDIO_MODEL})")
    ap.add_argument("--base-url", default=None, help=f"Audio API base URL (default: AUDIO_BASE_URL env or {AUDIO_BASE_URL})")
    ap.add_argument("--node-id", default=None, help="Only generate for one node id")
    ap.add_argument("--voice-prompt", default=None, help="Override voice design prompt for all nodes")
    args = ap.parse_args()

    api_key = AUDIO_API_KEY
    if not api_key:
        raise SystemExit("AUDIO_API_KEY not set. If using Mimo, set MIMO_API_KEY instead.")

    if AUDIO_PROVIDER != "mimo_chat_audio":
        raise SystemExit(f"Unsupported AUDIO_PROVIDER={AUDIO_PROVIDER!r}. Current built-in provider: mimo_chat_audio")

    base_url = args.base_url or AUDIO_BASE_URL

    data_path = Path(args.data_json)
    project_dir = data_path.parent
    out_dir = Path(args.output_dir) if args.output_dir else project_dir / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    _, nodes = find_nodes(data)
    generated = []

    for node in nodes:
        if args.node_id and node.get("id") != args.node_id:
            continue

        sound = node.get("sound", {})
        if not isinstance(sound, dict):
            continue

        voice = args.voice_prompt or node.get("voice_prompt") or ""
        if not voice:
            sound_desc = sound.get("description", "")
            style = data.get("meta", {}).get("style", "")
            voice = f"安静的叙述者声音，语速缓慢，语气克制内敛，有空间感和呼吸感。{style[:50]}"

        text = node.get("audio_text", "")
        if not text:
            text = sound.get("description", "")
        if not text:
            continue

        node_id = slug(node.get("id") or node.get("label") or "node")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = out_dir / f"{node_id}_{stamp}.wav"

        print(f"Generating audio for {node.get('id')}...", flush=True)
        try:
            size = generate_audio(voice, text, out_path, api_key, base_url, model=args.model)
            rel = out_path.relative_to(project_dir)
            audio = node.setdefault("audio", {})
            audio["url"] = str(rel)
            audio["status"] = "generated"
            audio["model"] = args.model
            audio["generated_at"] = datetime.now().isoformat(timespec="seconds")
            audio["duration_hint"] = f"~{len(text) / 4:.0f}s"
            generated.append(str(out_path))
            print(f"  OK: {out_path} ({size} bytes)")
        except Exception as e:
            print(f"  FAILED: {e}")

    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"generated": generated, "data_json": str(data_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
