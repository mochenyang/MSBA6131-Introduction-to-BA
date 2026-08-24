# Scene Planning: Chunking a Transcript for Pedagogical Clarity

This is the craft behind Step 2-3 of `/make-scene-plan`: turning spoken, linear narration into a sequence of deliberately chunked scenes that teach well when watched, not just a reformatted transcript.

## One idea per scene

A scene is the smallest unit of "the viewer can pause here and have learned one complete thing." Signs a transcript segment is really two scenes stitched together:
- It states a concept, then pivots to a worked example of a *different* concept.
- It makes a claim, then makes an unrelated second claim ("...and that's why X matters. Also, one thing to note is Y...").
- The instructor's own pacing has a clear seam — a summarizing sentence, a "so," a "now," a topic-shift phrase.

Signs two adjacent segments should be *merged* into one scene:
- The second segment is a direct continuation, clarification, or example of the first (a definition immediately followed by "so for example...").
- Splitting them would leave one half too short to stand alone as a beat (a single sentence of narration with nothing for the Visual to build toward).
- **The segments are all sub-steps of one bigger arc the viewer experiences as a single idea** — e.g. "motivating question → intuition → procedure → how to tune a parameter" for one algorithm, or "definition → concrete picture → why it matters." Don't split these just because each sub-step could technically stand alone; if a viewer would describe the whole span as "then it explained how k-NN works," it's one scene. Default to merging a whole such arc into one scene, with the sub-steps sequenced inside the Visual ("First show the naive rule... Next, narrow it to neighbors... Then the numbered procedure builds... Finally, a second list covers choosing k"). Reach for this default even when the combined Text is well past the usual scene-length heuristic below — length isn't the deciding signal here, arc-unity is. Split the arc back into separate scenes only when a sub-step needs its own callback target from a *later*, non-adjacent scene, or is long/dense enough that combining would blow well past a narratable single take.

There's no fixed target scene count, but bias toward fewer, denser scenes over more, thinner ones — an initial per-idea segmentation tends to fragment a coherent teaching arc into more scenes than the content actually needs, and consolidating related sub-beats after the fact is the single most common edit a reviewer makes. When deciding between splitting and merging a borderline case, merge. A dense 5-minute transcript covering six distinct ideas becomes six-plus scenes; a rambling 15-minute transcript that circles one idea repeatedly might become three. Idea density drives the count, not runtime.

## Cut scope, not just filler

Beyond removing ASR noise (see "Cleaning without flattening" below), actively look for whole spans of content that don't earn their place in *this* video's core arc, and cut them rather than compressing them:
- **Recap/summary scenes** ("to sum up, pros are X, cons are Y") — the preceding scenes already taught this; a separate recap scene rarely survives review. Omit by default unless the transcript's summary adds a genuinely new point.
- **Secondary worked examples that duplicate a procedure already shown.** If a scene already walks through "here's the numbered procedure, applied to this data," a second worked example re-applying the same procedure to slightly different numbers (e.g. "now with k=6 instead of k=3") is usually cut, not kept — the mechanism was already demonstrated.
- **Advanced complications tangential to the stated core arc.** A secondary technique/metric presented as "also, here's an alternative way to do this" (a second purity measure, a third stopping condition, a three-way data split when a two-way split already made the point) dilutes the main thread more than it adds. Keep the one version that carries the concept; flag the rest in the Step 5 report rather than including them, so the instructor can opt back in.
- **Forward-teasers for material this video doesn't actually cover.** Don't preview or name-drop techniques from later lectures unless the transcript follows through on them within this same transcript.
- **Long enumerations of examples/applications** — keep a representative handful that spans the space (e.g. one per major domain), not every instance the instructor mentioned.

When in doubt about a cut, don't silently drop it — note it in the Step 5 report as a proposed cut so the instructor can veto it, but default to leaving it out of the draft.

## Concrete before abstract

When a transcript introduces an abstract concept, look for whichever the instructor supplies — a concrete example, an analogy, a specific number — and sequence it to *motivate* the abstraction rather than illustrate it after the fact, when that's a genuine option:

1. Concrete scenario first (a specific, relatable case — "imagine you're a data scientist at Walmart looking at these customers...").
2. Formal definition second, now that the viewer has a mental anchor for what it's a definition *of*.
3. Contrast with an adjacent/confusable concept third, once the definition is solid enough to compare against something.

This is exactly the arc `1_Cluster Analysis/scene_plan.md` scenes 2-4 follow: concrete Walmart example → formal definition of clustering → contrast with classification. If the transcript already presents ideas in this order, keep it. If the instructor defined the term first and only later gave the example (common when lecturing live), consider resequencing — but only when the reorder is unambiguous and doesn't strand a "as I just said" or "building on that" reference in the wrong place.

**Concreteness is for motivating a new concept, not mandatory for every mechanism demo.** Once a concept is already established and a scene's only job is to illustrate a general mechanism (e.g. "here's how splitting the input space works," independent of any specific domain), a generic setup — abstract attributes (X1, X2), abstract classes (Class A / Class B, or a plain color pair) — is often the *better* choice, not a fallback: it signals "this generalizes to any attributes," where an arbitrary concrete domain (a specific pair of business attributes) can wrongly imply the mechanism is specific to that domain. Reserve concrete/domain grounding for scenes where the domain itself is doing pedagogical work — motivating why the concept matters, giving stakes to a metric (e.g. framing a confusion matrix around fraud detection so precision/recall feel consequential, not just definitional), or serving as the one running example per "One running example, reused" below. When a scene is purely mechanical, default to generic.

## One running example, reused

Pick one concrete example, dataset, or scenario from the transcript — ideally whatever the instructor already leans on — and reuse it across as many scenes as the content allows, rather than inventing a fresh example per scene. This does two things at once:
- **Pedagogically**: repetition on one mental model (the same customers, the same data points) is what lets later scenes build on earlier ones instead of re-paying the cost of a new setup every time.
- **Mechanically**: `/make-manim` shares state across scenes via `common.py` and reads "the same X as in scene N" as a fixture cross-reference. A scene plan that keeps reusing one example gives `/make-manim` a callback to build on; a scene plan that invents a new example every scene forces every scene to start from zero.

When a Visual reuses or evolves an earlier scene's visual, say so explicitly: `"the same scatter plot as in scene 2, now with each cluster circled"` — not `"a scatter plot showing clusters"`, which reads as a brand-new one.

## Cleaning without flattening

Raw transcripts carry: filler ("um," "you know," "right?"), false starts, mid-sentence restarts, repeated re-explanations of the same point, and asides that don't serve the current scene (a joke, a scheduling note, an aside about the exam). Cut all of that. But don't launder the instructor's actual voice out of the Text in the process — if their specific phrasing, analogy, or example is what makes a point land, keep it close to verbatim rather than replacing it with generic textbook language. The goal is a script that still sounds like this instructor teaching, just without the noise.

Watch for content that's *only* clear because of something on a whiteboard, a slide, or a hand gesture the transcript can't capture ("so this one goes here, and that means these two are basically the same"). Either recover the intended meaning from context and state it explicitly in the Text, or flag it in the Step 5 report as something to verify against the source material.

This applies even to an already-clean, written script, not just messy ASR transcripts: cut authorial meta-commentary that talks *about* the teaching rather than doing it — "the best way to introduce X is just to show you one," "the primary reason we care about Y is..." A clean script can still carry throat-clearing; remove it the same way you'd remove "um" and a false start, even though it's grammatical and wasn't a transcription artifact.

## Scene length heuristic

A scene's `**Text**` should be narratable in roughly 20-90 seconds — rough guide, not a hard rule (~50-220 spoken words, faster for a short punchy beat, slower for a formula walkthrough that needs pauses). If a candidate scene's Text is running well past that with no natural sub-point to split on, it's probably fine as-is (some ideas — a multi-part worked example — genuinely need the room). If it's running short with nothing for a Visual to do, look at merging it with a neighbor.

## Visual invention when the source is silent

Most transcript segments carry no explicit visual description — the instructor was just talking. Every scene still needs a Visual. Default patterns by scene type:
- **Definition** → the term and its definition as on-screen text, built up progressively (term first, then each defining clause).
- **Concrete example/scenario** → the actual entities/numbers from the Text, laid out spatially (not a generic icon standing in for "data").
- **Comparison/contrast** → split-screen or side-by-side, one label per side.
- **Process/mechanism** → step-by-step build, left-to-right or top-to-bottom matching the process's own order.
- **Formula/derivation** → the expression on screen, with terms highlighted as the Text introduces them one at a time.

Prefer whatever's concrete and specific to this scene's content over an abstract or decorative visual — see `.claude/skills/make-manim/references/visual_techniques.md`'s guidance on concreteness for the same principle applied on the `/make-manim` side.

## Worked example

**Raw transcript excerpt** (ASR-style, unedited):

> okay so, um, clustering — the basic idea, right, is you're trying to find groups in your data. like, so, so imagine you've got a bunch of customers, right, and some of them spend a lot and don't care about price, and some of them are like really price sensitive, they'll switch stores for a dollar off, um, and so what you want to do is find those groups automatically, you don't tell the algorithm what the groups are ahead of time, that's — that's the key thing actually, let me back up, that's actually really important, unlike, say, if you were building a model to predict whether someone's going to churn, there you already know the categories, churn or not churn, but clustering you don't know the groups in advance, the algorithm finds them

**Turned into scene plan entries** — this splits into two scenes (concrete example, then the defining contrast with predictive modeling), cutting the filler and the false-start-and-backup, but keeping the instructor's own churn example and "you don't tell the algorithm the groups ahead of time" framing:

```markdown
# Scene 4

**Text**: The basic idea of clustering is to find groups in your data. Imagine you've got a bunch of customers: some spend a lot and don't care about price, while others are so price-sensitive they'll switch stores over a dollar. Clustering is what lets you find groups like these automatically.

**Visual**: A scatter plot of customer dots fades in unsorted (single color). As the text describes the two customer types, two loose clusters of dots visually separate and take on distinct colors, with no boxes or labels yet -- the grouping should look discovered, not pre-drawn.

# Scene 5

**Text**: Here's the key thing about clustering: you don't tell the algorithm what the groups are ahead of time. That's different from, say, building a model to predict whether someone's going to churn -- there, you already know the categories: churn or not churn. With clustering, you don't know the groups in advance; the algorithm finds them.

**Visual**: Split-screen. Left, titled "Clustering": the same colored customer scatter from scene 4, with a "?" label where group names would go. Right, titled "Predicting Churn": a bar with two pre-labeled bins, "Churn" / "Not Churn", already drawn before any data point moves into either one.
```

Note what changed: filler and the mid-thought backup are gone; the two ideas (concrete example, defining contrast) are split into separate scenes because they're separate beats; the churn example and the instructor's own framing survived intact; and both Visuals are concrete and specific to this content, with scene 5 explicitly calling back to scene 4's scatter plot rather than inventing a new one.
