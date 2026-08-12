---
name: make-manim
description: "scene plan (numbered Text/Visual entries) -> scenes/ package of standalone, fast-to-recompile manim scene modules + a combined video script, following voiceover/manim conventions"
trigger: /make-manim
---

# /make-manim

Turn a scene plan into working `manim_voiceover` scene code, structured as one small standalone-runnable file per scene (fast to iterate on) plus a thin combined script that recomposes them into the full video (for final renders). 

## Usage

```
/make-manim <path/to/scene_plan.md>              # build scenes for a plan, inferring the unit folder from its location
/make-manim <path/to/unit-folder>                # same, looks for scene_plan.md inside that folder
/make-manim <path/to/unit-folder> --scene 5       # (re)build only scene 5, leave the rest untouched
/make-manim <path/to/unit-folder> --from 3        # (re)build scenes 3 onward, leave 1-2 untouched
```

If no path is given, look for a single `scene_plan.md` under the current directory (recursively, one level of unit-folder is fine) and ask the user to disambiguate if there's more than one.

## What a scene plan looks like

Plain markdown, one `# Scene N` heading per scene, each with a `**Text**:` (narration) and `**Visual**:` (what should be on screen) block:

```markdown
# Scene 3

**Text**: Market segmentation is a representative application of cluster analysis. ...

**Visual**: show definition of clustering in plain text. Then show the same scatter
plot as in scene 2 with the same clusters. Circle each cluster and add an
inward-pointing arrow labeled "high intra-similarity" ...
```

`**Visual**` is a natural-language sketch, not a spec — you have creative latitude in choosing the concrete manim objects/animations, but it must not contradict what's written there. When `**Visual**` references "the same X as in scene N", that is a cross-scene dependency — see the fixtures section below.

## Step 0: Get oriented

1. Read the scene plan in full before writing any code — later scenes routinely reference earlier ones ("the same scatter plot as scene 2", "recall the checklist from scene 5"). Note every such cross-reference up front.
2. Determine the unit folder (e.g. `1_Cluster Analysis/`) and the repo root (parent of the unit folder — this is where `tts.py` lives).
3. Check whether `<unit-folder>/scenes/` already exists. If yes, this is an incremental build (see `--scene`/`--from`) — read the existing `common.py` and neighboring scene files first so new scenes match established palette/helpers instead of redefining them.
4. Pick a combined-script name from the unit folder name: snake_case for the file (`association_rules.py`), PascalCase for the class (`AssociationRules`) — mirrors `cluster_analysis.py` / `ClusterAnalysis`.

## Step 1: Design shared state before writing scene files

Scan the plan for anything reused across scenes: a recurring diagram, a color-coded entity, a helper shape. Anything used by **two or more** scenes belongs in `<unit-folder>/scenes/common.py` as a free function or constant — not a method on some scene class, since scene files must not import from each other. Anything used by exactly **one** scene stays local to that scene's file (as a `@staticmethod` on its Mixin, same as `make_checklist_item` in `scene_05.py` or `add_bullet` in `scene_06.py` from the cluster-analysis example).

**Name every scene-local helper method uniquely across the whole unit** — prefix it with the scene number, e.g. `scene14_scatter_pos`, never a generic `scatter_pos`/`dend_xy`/`centroid_pos`. Each scene's Mixin lives in its own file and previews fine in isolation, but the combined script's class inherits *all* mixins into one class at once, and Python's MRO silently resolves same-named methods to whichever mixin is listed first among the combined class's bases — with no error at import or render time. Two scenes independently defining `def scatter_pos(i):` with different constants will both compile and both preview correctly standalone; in the combined video, one silently overrides the other. This is a real bug found in the cluster-analysis unit: scenes 10, 11, and 14 each had their own `scatter_pos` (and 10/13 their own `dend_xy`/`make_dend_u`), all with different layout constants — scene 10's versions silently won for all of them once combined, so scenes 11, 13, and 14 rendered with scene 10's positions/scale instead of their own. Generic-sounding names for position/coordinate helpers are the highest-risk case, since near-identical helpers recur naturally across scenes sharing the same dataset. See Step 5 for the check that catches this before handoff.

Also decide the color palette here (see `references/visual_techniques.md` → Color Palettes and Color as Meaning) and put every named color as a constant in `common.py`, e.g.:

```python
BRAND_LOYALIST_COLOR = RED
BUDGET_CONSTRAINED_COLOR = BLUE
```

Never hardcode a raw color for something that recurs across scenes — always go through the shared constant, so a later palette change is a one-line edit.

## Step 2: Write each scene as `scenes/scene_NN.py`

Two-digit, zero-padded (`scene_01.py`, ... `scene_12.py`). Each file has exactly this shape:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))              # scenes/ dir -> for `common`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent)) # repo root -> for `tts`

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import ...  # only what this scene actually uses


class SceneNNMixin:
    def scene_NN(self):
        ...  # the actual content: with self.voiceover(...): self.play(...)


class SceneNN(VoiceoverScene, SceneNNMixin):
    """Standalone preview: manim -pql scene_NN.py SceneNN"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        # ...fixtures for any state this scene depends on (see below)...
        self.scene_NN()
```

Rules:
- The mixin's `scene_NN` method is the single source of truth for that scene's content — it's used both by the standalone `SceneNN` class and by the final combined script. Never duplicate scene body code between them.
- Only import `common` names the scene actually references — don't blanket-import everything.
- If the scene needs numpy or other libs, import them normally after the `sys.path` block.
- Write the actual scene content following `references/visual_techniques.md` — load that file now if you haven't yet. In particular: progressive disclosure (build complexity step by step, matching how the `**Text**` unfolds), transform-don't-replace for related objects, deliberate color/spatial choices, and voiceover-driven timing (animations sum to a bit less than `tracker.duration`, absorb the rest with `self.wait(tracker.get_remaining_duration())`).

## Step 3: Handle cross-scene state with fixtures, not replays

If scene N's `**Visual**` depends on something built in an earlier scene (e.g. "the same scatter plot as scene 2"), the earlier scene's mixin should stash the needed mobjects as `self.<name>` at the point they're finished with (see `self.customer_plot = plot` at the end of `scene_02.py`'s `scene_02` method in the cluster-analysis example), and the later scene reads `self.<name>` assuming it's already set (that's true when running the combined script, since scenes execute in order on one instance).

For the later scene's **standalone** runner to work in isolation, add a `_fixture_scene_MM(self)` method on its `SceneNN` class that reconstructs just the needed end-state directly — call the same `common.py` helper functions the earlier scene used, skip all narration/animation, and `self.add(...)` the result so it's immediately visible (matching what the audience would see at that point in the real video). Call it from `construct()` before `self.scene_NN()`. Do **not** make the fixture call the earlier scene's own `scene_MM()` method — replaying a full voiceover scene just to get into the right state defeats the purpose of fast standalone iteration (it re-triggers TTS calls and the full animation timeline).

If a scene depends only on "the title text still being on screen" or similarly trivial state, the fixture can just construct and `self.add()` a stand-in directly (see `_fixture_scene_01` in `scene_02.py` of the cluster-analysis example) — it doesn't need to be pixel-perfect, just present so operations like `FadeOut` have something real to act on.

## Step 4: Write/update the combined script

At `<unit-folder>/<snake_case_name>.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from scenes.scene_01 import Scene01Mixin
from scenes.scene_02 import Scene02Mixin
# ... one import per scene ...


class <PascalCaseName>(
    VoiceoverScene,
    Scene01Mixin,
    Scene02Mixin,
    # ... in scene order ...
):
    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_01()
        self.scene_02()
        # ... in scene order ...
```

If `scenes/__init__.py` doesn't already exist (empty file), create it — it's what makes `scenes` importable as a package from the combined script.

For `--scene N` / `--from N` runs, only touch the specific `scenes/scene_NN.py` file(s) requested; still update the combined script's import/inheritance list if scenes were added or removed, but leave untouched scenes' files exactly as they are.

## Step 5: Validate before handing back

1. Syntax-check every new/changed file: `python -c "import ast; ast.parse(open(path).read())"` (or `py_compile`).
2. Import-check them for real (catches missing `common` names, bad manim symbols, etc.) — insert the unit folder and repo root onto `sys.path` and `importlib.import_module` each `scenes.scene_NN` plus the combined module. This does not require an API key.
3. Smoke-test render **at most 1-2 of the newly-written/changed scenes**, standalone, lowest quality, e.g.:
   ```
   manim -ql --disable_caching "<unit-folder>/scenes/scene_04.py" Scene04
   ```
   Do not render every scene and do not render the combined script during validation — each `with self.voiceover(...)` block makes a real OpenAI TTS call, so a full-video render burns real time and API cost. Prefer rendering whichever new scene has a fixture dependency (highest risk of a subtle bug) plus one independent scene. Full-video renders are the user's call, not something to run automatically.
4. Scan the combined class for method-name collisions across mixins — this is the check for the pitfall described in Step 1 (a helper silently overridden across scenes, invisible in every standalone preview and in syntax/import checks, only breaking the actual combined render). Run once after any new/changed scene touches a `@staticmethod`/helper method:
   ```python
   import sys; sys.path.insert(0, "<unit-folder>")
   from <snake_case_name> import <PascalCaseName>
   seen = {}
   for cls in reversed(<PascalCaseName>.__mro__):
       for name, val in cls.__dict__.items():
           if callable(val) and not name.startswith("__") and not name.startswith("scene_") and name != "construct":
               if name in seen and seen[name] is not cls:
                   print("COLLISION:", name, seen[name], "overridden by", cls)
               seen[name] = cls
   ```
   Any printed collision means the combined-video render silently uses the wrong scene's version of that helper. Fix by renaming to a scene-prefixed name (Step 2's naming rule) in every colliding file and re-running until nothing prints.
5. Report which scenes were built/changed, which (if any) were smoke-rendered, and remind the user of the per-scene preview command and the full-render command for the combined script.

## Reference

Load `references/visual_techniques.md` before writing scene content (Step 2) — it covers progressive disclosure, color/spatial semantics, animation idioms (`Indicate`, `Circumscribe`, `TransformMatchingTex`, ...), layout templates, and timing guidelines in more depth than fits here.
