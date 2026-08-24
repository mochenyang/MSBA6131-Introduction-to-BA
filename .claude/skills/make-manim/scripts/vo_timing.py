#!/usr/bin/env python3
"""
vo_timing.py -- sync helper for manim_voiceover scenes.

Manim's `self.voiceover(text=...)` blocks give you `tracker.duration` at
render time, but while *writing* a scene you don't have that number yet, and
even after rendering, eyeballing "where in this 25-second sentence does the
word 'entropy' land" by hand is slow and error-prone. This script does that
math for you, in two modes:

  duration  -- how long a line of narration takes to speak. Uses the real
              cached TTS clip if this exact text has already been rendered
              once (via manim_voiceover's media/voiceovers/cache.json +
              ffprobe); otherwise falls back to a calibrated words-per-second
              estimate so you can plan timing *before* the first render.

  mark      -- given the full narration text and one or more marker phrases
              (substrings that appear in it), estimate the timestamp (in
              seconds) where each marker starts and ends, by word position
              proportional to total duration. This is a heuristic (no
              forced word-alignment is configured in this project's
              tts.py -- transcription_model=None), but it's far better than
              guessing, and it's what actually fixed several "audio out of
              sync" bugs in the Predictive Analytics I unit.

Usage
-----
Estimate before ever rendering (no cache needed):
    python3 vo_timing.py duration "Some narration text here."

After the scene has been rendered at least once (uses the real clip):
    python3 vo_timing.py duration "Some narration text here." --media-dir media/voiceovers

Find where phrases land in the (real or estimated) timeline:
    python3 vo_timing.py mark "Full narration sentence goes here." \\
        "first phrase" "second phrase" --media-dir media/voiceovers

Run from wherever you run `manim` from (usually the repo root) -- that's
where media/voiceovers/cache.json ends up after a render, since manim's
media dir is relative to the process's cwd, not the scene file's location.

Workflow
--------
1. While first writing a scene, use `duration` (no --media-dir, or one
   that doesn't exist yet) to sanity-check that your planned run_times +
   waits stay safely under the estimated duration for each voiceover block.
2. Smoke-render the scene once (per SKILL.md Step 5). This populates
   media/voiceovers/cache.json with the real TTS clips.
3. Re-run `duration` / `mark` with --media-dir pointing at that cache to
   get the *real* clip length and retime precisely -- especially for any
   voiceover block where multiple visual beats need to land on specific
   words (e.g. revealing icons/labels as each is named).
4. If you edit the narration text afterward, the cache entry for the old
   text becomes stale for the new text (cache is keyed by exact text) --
   expect a fallback to the estimate until you re-render.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import difflib
from pathlib import Path

# Calibrated from real OpenAI tts-1 "alloy" clips (speed=1.0, this repo's
# tts.py default) across ~50 sampled sentences during Predictive Analytics I
# sync fixes: observed range was ~0.35-0.51 s/word depending on punctuation
# density and word length. 0.40 is a reasonable middle estimate for planning
# *before* a real render exists -- always prefer the real cached duration
# once available.
DEFAULT_SECONDS_PER_WORD = 0.40


def load_cache(media_dir: Path):
    cache_path = media_dir / "cache.json"
    if not cache_path.exists():
        return {}
    with open(cache_path) as f:
        entries = json.load(f)
    by_text = {}
    for entry in entries:
        by_text[entry["input_text"].strip()] = entry["final_audio"]
    return by_text


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def get_duration(text: str, media_dir: Path | None):
    """Returns (duration, source) where source is 'cached', 'fuzzy', or 'estimated'."""
    text = text.strip()
    words = text.split()
    estimate = len(words) * DEFAULT_SECONDS_PER_WORD

    if media_dir is None:
        return estimate, "estimated"

    by_text = load_cache(media_dir)
    if not by_text:
        return estimate, "estimated"

    fname = by_text.get(text)
    source = "cached"
    if fname is None:
        matches = difflib.get_close_matches(text, by_text.keys(), n=1, cutoff=0.85)
        if matches:
            fname = by_text[matches[0]]
            source = "fuzzy"
        else:
            return estimate, "estimated"

    audio_path = media_dir / fname
    if not audio_path.exists():
        return estimate, "estimated"

    try:
        return ffprobe_duration(audio_path), source
    except (subprocess.CalledProcessError, ValueError):
        return estimate, "estimated"


def normalize_word(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def find_marker(words_norm: list[str], marker: str):
    """Find the marker phrase as a contiguous subsequence of words_norm.
    Returns (start_idx, end_idx_inclusive) or None if not found."""
    marker_words = [normalize_word(w) for w in marker.split() if normalize_word(w)]
    if not marker_words:
        return None
    n, m = len(words_norm), len(marker_words)
    for i in range(n - m + 1):
        if words_norm[i:i + m] == marker_words:
            return i, i + m - 1
    return None


def cmd_duration(args):
    media_dir = Path(args.media_dir) if args.media_dir else None
    duration, source = get_duration(args.text, media_dir)
    word_count = len(args.text.split())
    print(f"duration: {duration:.3f}s  ({source}, {word_count} words, "
          f"{duration / max(word_count, 1):.3f}s/word)")


def cmd_mark(args):
    media_dir = Path(args.media_dir) if args.media_dir else None
    duration, source = get_duration(args.text, media_dir)
    words = args.text.split()
    words_norm = [normalize_word(w) for w in words]
    total = len(words)

    print(f"total duration: {duration:.3f}s  ({source}, {total} words)")
    print()
    for marker in args.markers:
        hit = find_marker(words_norm, marker)
        if hit is None:
            print(f"  [NOT FOUND] {marker!r}")
            continue
        start_idx, end_idx = hit
        t_start = (start_idx / total) * duration
        t_end = ((end_idx + 1) / total) * duration
        print(f"  {marker!r}")
        print(f"      starts ~{t_start:.2f}s (word {start_idx + 1}/{total})")
        print(f"      ends   ~{t_end:.2f}s (word {end_idx + 1}/{total})")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--media-dir", default=None,
        help="Path to manim_voiceover's media/voiceovers directory (contains cache.json). "
             "Omit to always use the word-count estimate (e.g. before the first render).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_dur = sub.add_parser("duration", help="Get a voiceover line's duration (real if cached, else estimated).")
    p_dur.add_argument("text", help="The exact voiceover text.")
    p_dur.set_defaults(func=cmd_duration)

    p_mark = sub.add_parser("mark", help="Estimate timestamps for marker phrases within a voiceover line.")
    p_mark.add_argument("text", help="The exact voiceover text.")
    p_mark.add_argument("markers", nargs="+", help="One or more phrases (substrings of text) to locate in time.")
    p_mark.set_defaults(func=cmd_mark)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
