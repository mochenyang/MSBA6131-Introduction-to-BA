# Visual Techniques for Math/Concept Animation

Load this file when actually writing scene *content* (the body of a `scene_NN` method). It's the taste layer on top of the architecture described in SKILL.md — the architecture makes scenes easy to compile and recombine, this makes them good to watch.

## Core Principles

### 1. Progressive Disclosure
Never show everything at once. Build complexity gradually.

- **Bad:** show the complete equation/diagram immediately.
- **Good:** build it piece by piece, explaining each part as it appears.

```
1. Show simple case: f(x) = x²
2. Add complexity: f(x) = ax²
3. Full form: f(x) = ax² + bx + c
```

### 2. Transform, Don't Replace
When one object evolves into a related one, morph it rather than cutting away.

- **Bad:** `FadeOut(equation1)`, `FadeIn(equation2)`
- **Good:** `TransformMatchingTex(equation1, equation2)` or `FadeTransform(a, b)`

This keeps visual continuity and shows *how* the forms relate. Reserve plain `FadeOut`/`FadeIn` for when objects are conceptually unrelated (e.g. moving to a new topic).

### 3. Color as Meaning
Pick colors deliberately and reuse them consistently for the rest of the video — never recolor the same concept differently between scenes.

Two coloring patterns show up, and a scene plan usually needs both:

- **Entity colors** — when the script has recurring named things (e.g. three customer segments, two clusters), give each one a fixed color the moment it's introduced and never reuse that color for anything else. Define these as named constants in `scenes/common.py` (e.g. `BRAND_LOYALIST_COLOR = RED`) so every scene file that touches that entity imports the same constant — this is what keeps a callback in scene 6 visually recognizable as "the same thing" from scene 2.
- **Semantic colors** — for generic roles that recur across many different topics:
  - Input/given values: `BLUE`
  - Output/result: `GREEN`
  - Term currently being discussed: `YELLOW` highlight
  - Error/negative/warning: `RED`
  - Neutral/supporting/background: `WHITE` / `GREY`

If a scene plan's visual notes don't specify colors, default to the semantic palette above rather than inventing new ones per scene.

### 4. Spatial Relationships
Position encodes relationships — use this instead of (or alongside) color:

- **Left-to-right**: transformation, time, causation, before/after
- **Top-to-bottom**: hierarchy, derivation, drill-down
- **Center**: current focus of attention
- **Periphery**: context, reference, things not currently active

---

## Animation Techniques

### Highlighting & Focus
- `Indicate(mob)` — brief flash, use for a light "notice this"
- `Circumscribe(mob, color=YELLOW)` — circle/box drawn around an element
- `FlashAround(mob)` — more dramatic, reserve for a punchline/reveal moment
- `Wiggle(mob)` — draws attention without implying anything changed

Don't stack more than one of these on the same beat — pick the one that matches how important the moment is.

Use `Indicate` sparingly, especially on text. It's tempting to reach for it every time the narration names something on screen, but a scene that indicates every label, term, or data point it mentions trains the eye to ignore the flash — by the third or fourth one it's just noise, and the moments that actually need emphasis no longer stand out. Reserve it for a genuinely singular beat (the one point about to be used in a calculation, the one term the whole scene pivots on) rather than a reflex for every noun the voiceover touches. For routine "here's the next thing" beats, let entrance animations (`Write`, `FadeIn`) and the narration's own pacing carry the attention instead — they introduce something new without also claiming it's especially important.

### Equation Manipulation
- Isolate terms with `set_color_by_tex(...)` before drawing attention to a specific part.
- For step-by-step derivations, build each `MathTex` step so substrings match the previous step's substrings, then use `TransformMatchingTex` between them — this auto-aligns the parts that didn't change.
- For substitution, animate the actual value moving into the variable's on-screen position rather than just replacing the whole expression.

### Geometric Intuition
- Always label axes (`axes.get_axis_labels(...)` or explicit `Text` labels) — an unlabeled `Axes()` is a code smell.
- `TracedPath(dot.get_center, stroke_color=...)` to show how a moving point traces a curve.
- `axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.5)` for integrals/sums.

### 3D Techniques (only when the scene plan calls for 3D)
- Orbit the camera to reveal structure: `self.play(frame.animate.reorient(60, 70), run_time=3)`.
- Show a 2D projection/shadow alongside the 3D object to connect back to 2D formulas.
- Slice through the object to expose cross-sections when that's the point being made.

### Code / Pseudocode Blocks
**Do not use manim's `Code` mobject** (`from manim import Code`, the pygments-backed syntax-highlighter) — confirmed broken in this project's installed manim version (0.20.1): rendered standalone with a plain 5-line snippet, it overlapped two lines on top of each other and silently dropped the last line entirely from view, with no error at construction or render time. This is exactly the kind of bug that's invisible until you actually look at the rendered frame.

For pseudocode/code-like text, build it from plain `Text` lines instead, arranged with `.arrange(DOWN, aligned_edge=LEFT, buff=...)` inside a `SurroundingRectangle`, and get lightweight keyword coloring via `Text`'s `t2c` param (text-to-color dict), e.g.:

```python
Text("while True:", font_size=22, t2c={"while": PURPLE_B, "True": PURPLE_B})
```

This reads as "syntax-highlighted" enough for a pseudocode box without depending on the broken mobject. If a future manim upgrade might have fixed `Code`, verify by rendering a multi-line snippet standalone and inspecting the actual frame (not just checking it imports/constructs without error) before trusting it in a real scene.

### Small Font Sizes
**`Text(..., font_size=X)` with `X` well under ~40 renders with visible glyph-spacing artifacts** in this project's manim version — confirmed empirically: `Text("Training Error", font_size=40)` renders clean; the same string at `font_size=14` renders as "Train in g Error", with gaps appearing *inside* words (not at word boundaries) rather than at consistent letter positions. This is a real, silent bug: no error, no warning, just wrong-looking text — the kind of thing that's easy to miss in a quick render check and only shows up on close frame inspection. Root cause: manim's `Text` is Pango-backed, and small-font glyph rasterization rounds each character's advance-width to the pixel grid before manim lays out the per-character submobjects from that data; at large sizes the rounding error is a negligible fraction of letter width, at small sizes it's a large enough fraction to be visible.

Nearly every scene ends up wanting a legend, footnote, axis label, or node label well under 40 — so fix this once per unit rather than per call site. Define this in `common.py` (see Step 1) and have every scene file import `Text` from `common` instead of `manim`:

```python
from manim import Text as _ManimText

TEXT_SAFE_BASE_SIZE = 40

class Text(_ManimText):
    def __init__(self, text, font_size=48, **kwargs):
        if font_size < TEXT_SAFE_BASE_SIZE:
            super().__init__(text, font_size=TEXT_SAFE_BASE_SIZE, **kwargs)
            self.scale(font_size / TEXT_SAFE_BASE_SIZE)
        else:
            super().__init__(text, font_size=font_size, **kwargs)
```

Every existing `Text(..., font_size=14)` call site keeps its exact signature — only the import changes (`from common import Text, ...` placed after `from manim import *`, so it shadows manim's name). Since this class definition also shadows `Text` within `common.py`'s own module namespace, every `Text(...)` call inside shared helpers there (`make_tree_node`, `make_confusion_matrix`, etc.) picks up the fix automatically too, with no changes to those helpers needed. `MathTex`/`Tex` are LaTeX-rendered, not Pango, and are unaffected — this fix is `Text`-only.

---

## Common Visual Metaphors
Reach for these defaults unless the scene plan specifies something else:

- **Vectors** → arrows from the origin; addition → tip-to-tail; scaling → stretch/shrink.
- **Functions** → a "machine": input enters one side, transformation happens, output exits the other.
- **Matrices** → grid transformation; track where the basis vectors land; determinant = area/volume scaling.
- **Derivatives** → tangent line touching the curve; zoom in to show local linearity; animate the slope as the point moves.
- **Integrals** → Riemann rectangles, width → 0, area filling in under the curve.

---

## Scene Composition Layouts

Pick a layout deliberately per scene, don't default to "everything centered."

**Title + main + formula** (good for a single concept building to a formula):
```
┌─────────────────────────────────┐
│           TITLE/CONTEXT         │  top edge
├─────────────────────────────────┤
│      MAIN VISUALIZATION         │  center, largest area
├─────────────────────────────────┤
│    EQUATION / FORMULA           │  bottom third
└─────────────────────────────────┘
```

**Side-by-side comparison** (good for "A vs B", "before vs after"):
```
┌───────────────┬───────────────┐
│   BEFORE /    │   AFTER /     │
│   CONCEPT A   │   CONCEPT B   │
└───────────────┴───────────────┘
```

**Zoomed detail** (good for "here's the subtle part"):
```
┌─────────────────────────────────┐
│  ┌─────┐                        │
│  │ZOOM │ ←── magnified detail   │
│  └─────┘                        │
│         Main context            │
└─────────────────────────────────┘
```

---

## Timing Guidelines

| Action | Typical `run_time` |
|--------|------------------|
| Simple shape creation | 0.5-1s |
| Text/equation writing | 1-2s |
| Transformation | 1-2s |
| Camera movement | 2-3s |
| Pause for absorption | 0.5-1s |
| Complex/multi-part animation | 2-4s |

**Rhythm pattern:** fast-fast-SLOW-fast-fast-SLOW. Quick animations for setup and connective tissue, slow down specifically on the beat that carries the key insight — don't let every animation run at the same speed, that reads as monotone.

When narration drives timing (this repo uses `manim_voiceover`), animation `run_time`s should sum to a bit less than the voiceover's spoken duration, with the remainder absorbed by `self.wait(tracker.get_remaining_duration())` at the end of the `with self.voiceover(...)` block — never let an animation visibly finish and then sit idle for seconds with nothing happening before the line ends, and never let the animation still be running after the line has finished.

---

## Color Palettes

Pick one palette per unit/module and put its values in `scenes/common.py`; don't mix palettes within one video.

**Classic 3b1b** (warm, approachable):
- Background: `#1C1C1C` · Primary: `#58C4DD` (blue) · Secondary: `#83C167` (green) · Accent: `#FFFF00` (yellow) · Warning: `#FF6666` (red)

**High contrast** (best for screen-recorded/small-text-heavy content):
- Background: `#000000` · Primary: `#FFFFFF` · Accent: `#FFD700`

**Soft academic** (lecture-style, easier on the eyes for long videos):
- Background: `#2D2D2D` · Primary: `#6ECFFF` · Secondary: `#98E898` · Accent: `#FFE66D`

Manim's default background is already close to the "Classic 3b1b" dark grey — only override it (`self.camera.background_color = ...`) if the scene plan or user asks for a different look.
