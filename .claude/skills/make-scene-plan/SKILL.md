---
name: make-scene-plan
description: "instructor script / narration / lecture transcript -> scene_plan.md (numbered Text/Visual scenes), structured for pedagogical clarity as input to /make-manim"
trigger: /make-scene-plan
---

# /make-scene-plan

Turn a raw instructor script, lecture narration, or recording transcript into a `scene_plan.md` — the numbered `# Scene N` / `**Text**` / `**Visual**` document that the `/make-manim` skill (`.claude/skills/make-manim/SKILL.md`) turns into an actual narrated video.

This skill produces the **content plan**; `/make-manim` produces the **manim code**. Run this one first. The two skills share one contract: the file this skill writes must be structurally identical to what `/make-manim` already knows how to consume (see `1_Cluster Analysis/scene_plan.md` for a working example).

## Usage

```
/make-scene-plan <path/to/transcript.txt>                        # infer/propose a unit folder from the transcript's topic
/make-scene-plan <path/to/transcript.txt> <path/to/unit-folder>  # write scene_plan.md into a specific unit folder (existing or new)
```

The input is whatever the instructor has: a written script, a cleaned-up narration doc, or a raw ASR transcript of a recorded lecture (timestamps, filler words, false starts, and all).

## Step 0: Read the whole input before writing anything

Read the entire transcript first — don't process it in a rolling window. Instructor transcripts routinely circle back ("actually, let me back up"), answer a question that arrived out of order, or state the punchline before the setup. You need the whole shape of the argument before you can decide how to chunk it, and cross-scene callbacks later depend on already knowing what the transcript reuses.

Identify:
- The topic/title (for naming the unit folder if one wasn't given).
- One concrete running example the transcript uses (a dataset, a scenario, a numeric case). If it has one, plan to reuse it across scenes rather than inventing a fresh example per scene — see `references/scene_planning.md` for why.
- Any figures, formulas, or comparisons the instructor gestures at verbally ("as you can see here...", "so we'd have two columns...") even though no visual exists yet — these are strong hints for the Visual field.

## Step 1: Determine the destination

If a unit folder wasn't given: look at the repo root for existing numbered unit folders (e.g. `1_Cluster Analysis/`) and propose the next number with a title-cased name in the same style (`2_Predictive Analytics/`). Confirm the folder name with the user before creating it — don't silently invent a topic title they didn't write.

If a `scene_plan.md` already exists at the destination, confirm with the user before overwriting it (they may want it appended to, merged, or diffed against instead).

## Step 2: Segment into a teaching sequence, not a transcript

This is the core judgment call in this skill — load `references/scene_planning.md` now before drafting scenes. In brief: a transcript is spoken and linear; a scene plan is a sequence of deliberately chunked, one-idea beats designed to be watched and absorbed. Segmenting means deciding where one idea ends and the next begins, cutting filler and digressions, occasionally resequencing for a cleaner narrative arc, and never force-fitting a fixed scene count — the transcript's actual idea density determines how many scenes come out.

Default toward fewer, denser scenes. A whole arc — motivating question, intuition, procedure, worked example, tuning a parameter — is normally *one* scene with a multi-part Visual, not one scene per sub-step; see "Merge aggressively across sub-beats of one bigger idea" in the reference doc. Also actively cut recap/summary scenes, redundant secondary examples, and tangential complications rather than including everything the transcript touches — see "Cut scope, not just filler" in the same doc. When unsure whether to split or merge, or whether to include or cut, merge and cut, then flag the call in the Step 5 report.

## Step 3: Draft each scene

For each scene, write:

- **Text** — the narration, in the instructor's own voice and phrasing wherever that's already clear, with filler/false-starts/repetition removed and any out-of-order material resequenced. This is a cleanup and restructuring pass, not a rewrite into generic textbook prose — if the instructor's own analogy or phrasing is what makes the point land, keep it. One or more paragraphs (blank-line separated) are fine within a single `**Text**:` block, matching the existing example.
- **Visual** — a natural-language sketch of what's on screen: what appears, in what order, what gets highlighted or transformed, and (when relevant) an explicit callback like "the same scatter plot as in scene 2." This is intent, not a manim spec — leave the concrete mobject/animation choices to `/make-manim`. Skim `.claude/skills/make-manim/references/visual_techniques.md` if you're unsure what's realistically stageable, but don't over-specify implementation details here.

Every scene needs both fields, even scenes whose transcript segment is pure narration with no visual cues in the source — invent a Visual that reinforces that scene's specific idea (a definition scene gets the definition in on-screen text; a comparison gets a split-screen; a worked formula gets terms highlighted as they're introduced), never a generic placeholder.

## Step 4: Write `scene_plan.md`

Match this structure exactly (see `1_Cluster Analysis/scene_plan.md` for the reference example):

```markdown
# Scene 1

**Text**: <narration, one or more paragraphs>

**Visual**: <one paragraph, natural-language sketch>

# Scene 2

**Text**: <narration>

**Visual**: <sketch>
```

- One `# Scene N` heading per scene, numbered sequentially from 1.
- `**Text**:` and `**Visual**:` are the literal labels `/make-manim` looks for — don't rename or reformat them.
- A blank line separates paragraphs within `**Text**:`, and separates the `**Text**` block from the `**Visual**` line.

Write the file to `<unit-folder>/scene_plan.md`.

## Step 5: Hand back for review

This skill does not invoke `/make-manim` automatically — the transformation from transcript to teaching script is a content decision (fidelity to what the instructor actually meant, tone, emphasis) that benefits from a human read-through before code gets generated from it. Report:
- How many scenes were produced and the destination path.
- Any places where you resequenced content, invented a Visual with no source cue, cut a substantial digression, or were unsure about instructor intent — flag these explicitly so review is fast and targeted rather than a full re-read.
- **Content you cut or merged away rather than including**, so the instructor can opt back in: recap/pros-and-cons scenes you omitted, secondary worked examples you dropped as redundant, secondary techniques/metrics/complications you left out in favor of one core version, and any transcript segments you folded into a bigger scene that could plausibly have stood alone. This list is usually more useful to the review pass than the "what's in the file" summary, since it's exactly what a reviewer would otherwise have to reconstruct by diffing against the transcript.
- The reminder that `/make-manim <unit-folder>` is the next step once the plan looks right.

## Reference

Load `references/scene_planning.md` before Step 2 — it covers the concrete-before-abstract pattern, chunking heuristics (scene length, when to split vs. merge), the running-example convention, and a worked before/after example of turning a messy transcript excerpt into scene plan entries.
