# MSBA6131 - Introduction to Business Analytics

Teaching materials for MSBA 6131, Introduction to Business Analytics. Each numbered folder (e.g. `1_Cluster Analysis/`) is a self-contained unit that builds a narrated `manim` video explaining one topic.

This repo is set up so that videos are never hand-animated in one giant script. Instead, each unit has a `scene_plan.md` (a plain-language script) that gets turned into one small, independently-previewable Python file per scene, plus a combined script that stitches them into the final video. See [The `/make-manim` skill](#the-make-manim-skill) below for how that works.

## Prerequisites

- **Python 3.12+** (pinned via `.python-version`)
- **[uv](https://docs.astral.sh/uv/)** for dependency management
- **ffmpeg** — required by `manim` to encode video. Install via your system package manager (`sudo apt install ffmpeg`, `brew install ffmpeg`, etc.)
- **A LaTeX distribution** — required for any scene using `MathTex`/`Tex`. [TinyTeX](https://yihui.org/tinytex/) is the lightweight option:
  ```bash
  wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
  export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"   # add to your shell profile
  ```
- **An OpenAI API key** — scenes are narrated with `manim-voiceover`'s OpenAI text-to-speech backend, so rendering any scene with a `self.voiceover(...)` block makes a real (billed) API call.

## Installation

Clone the repo and simply do

```bash
uv sync                # creates .venv/ and installs manim, manim-voiceover, python-dotenv, etc.
```

Create a `.env` file in the repo root (never committed — it's in `.gitignore`) with your OpenAI key:

```
OPENAI_API_KEY=sk-...
```

Then either activate the environment (`source .venv/bin/activate`) or prefix every command below with `uv run`.

### Rendering a video

Every scene file is runnable on its own for fast iteration, and every unit folder has a combined script for the final render.

```bash
# Preview a single scene at low quality (fast, opens a player when done)
uv run manim -pql "1_Cluster Analysis/scenes/scene_03.py" Scene03

# Render the full combined video for a unit, at low quality
uv run manim -ql "1_Cluster Analysis/cluster_analysis.py" ClusterAnalysis

# Final high-quality render (slow, use once you're happy with the low-quality pass)
uv run manim -qh "1_Cluster Analysis/cluster_analysis.py" ClusterAnalysis
```

`-ql`/`-qh` control render quality (low/high — see `manim -h` for the full list); `-p` opens the result automatically when done. Rendered output goes to a `media/` folder next to whatever file you rendered — these are git-ignored, since they're regenerable and often large (TTS audio gets cached under `media/voiceovers/`, so re-renders of unchanged narration are fast and don't re-hit the OpenAI API).

## Folder structure

```
.
├── tts.py                       # shared helper: builds the OpenAI TTS voice service, reads OPENAI_API_KEY from .env
├── pyproject.toml / uv.lock     # dependencies (manim, manim-voiceover, python-dotenv)
├── .claude/skills/make-manim/   # the /make-manim skill (see below)
└── 1_Cluster Analysis/          # one folder per teaching unit, numbered in viewing order
    ├── scene_plan.md            #   the script: one `# Scene N` heading per scene, with **Text** (narration) and **Visual** (what's on screen)
    ├── cluster_analysis.py      #   combined script: imports every scene and plays them in order for the final render
    └── scenes/                  #   one file per scene, each independently previewable
        ├── __init__.py
        ├── common.py            #     shared constants/helpers used by 2+ scenes (palettes, shared datasets, reusable mobject builders)
        ├── scene_01.py
        ├── scene_02.py
        └── ...
```

Each `scenes/scene_NN.py` follows the same shape: a `SceneNNMixin` class holding a `scene_NN(self)` method (the actual content — this is the single source of truth, used both standalone and in the combined script), and a thin `SceneNN(VoiceoverScene, SceneNNMixin)` wrapper for standalone preview. The unit's combined script (e.g. `cluster_analysis.py`) inherits every scene's mixin into one class and calls each `scene_NN()` method in order.

To add a new unit, create a new numbered folder with a `scene_plan.md` following the same format as the cluster analysis one, and hand it to the `/make-manim` skill.

## The `/make-manim` skill

`.claude/skills/make-manim/` is a [Claude Code skill](https://docs.claude.com/en/docs/claude-code) — a packaged set of instructions Claude follows when you invoke `/make-manim` in this repo. It turns a `scene_plan.md` into the `scenes/` package and combined script described above, so you don't have to hand-write manim boilerplate for every scene. This skill relies on (and modifies) a visual technique guide kindly shared by [this GitHub project](https://github.com/adithya-s-k/manim_skill/blob/main/skills/manim-composer/references/visual-techniques.md)

**Example Usage** (inside Claude Code, in this repo):

```
/make-manim <path/to/scene_plan.md>          # build every scene for a unit
/make-manim <path/to/unit-folder>            # same, looks for scene_plan.md inside
/make-manim <path/to/unit-folder> --scene 5  # rebuild only scene 5
/make-manim <path/to/unit-folder> --from 3   # rebuild scenes 3 onward
```

What it does, roughly:

1. Reads the whole `scene_plan.md` first, noting any cross-scene references ("the same scatter plot as scene 2") before writing anything.
2. Designs shared state up front — anything reused across 2+ scenes (colors, datasets, helper shapes) goes into `scenes/common.py`; anything scene-specific stays local to that scene's file.
3. Writes each scene as its own `scenes/scene_NN.py`, following the visual-design conventions in `.claude/skills/make-manim/references/visual_techniques.md` (progressive disclosure, deliberate color/spatial semantics, voiceover-driven timing, when to use `Indicate` vs `Circumscribe` vs `FlashAround`, etc.).
4. Handles cross-scene dependencies via lightweight "fixtures" (a scene that needs an earlier scene's end-state reconstructs just that end-state directly for its standalone preview, rather than replaying the whole earlier scene and its narration).
5. Writes/updates the unit's combined script.
6. Validates everything: syntax-checks and import-checks every changed file, smoke-renders 1-2 scenes at low quality, and scans for a specific pitfall — two scenes accidentally defining a same-named helper method, which silently breaks in the *combined* render even though every scene previews fine on its own (Python's MRO quietly picks one scene's version for all of them). It does **not** render every scene or the full combined video automatically, since every `voiceover(...)` block is a real, billed TTS call — full renders are something you trigger yourself once you're happy with the low-quality previews.

If you're building a new unit, just write a `scene_plan.md` in the same `# Scene N` / `**Text**` / `**Visual**` format as `1_Cluster Analysis/scene_plan.md` and run `/make-manim` on it.
