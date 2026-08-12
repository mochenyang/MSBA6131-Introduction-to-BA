import numpy as np
from manim import *

# Shared palette for the three Walmart customer segments, reused whenever
# that scatter plot recurs (definition-of-clustering, cohesion/separation, etc.)
BRAND_LOYALIST_COLOR = RED
BUDGET_CONSTRAINED_COLOR = BLUE
PRICE_SENSITIVE_COLOR = GREEN


def make_customer_axes():
    axes = Axes(
        x_range=[0, 10, 1],
        y_range=[0, 10, 1],
        x_length=6.2,
        y_length=5,
        axis_config={"include_ticks": False, "include_numbers": False},
    )
    x_label = axes.get_x_axis_label(
        Text("Price Sensitivity", font_size=26), edge=RIGHT, direction=RIGHT, buff=0.3
    )
    y_label = axes.get_y_axis_label(
        Text("Shopping Budget", font_size=26), edge=UP, direction=LEFT, buff=0.3
    )
    return axes, x_label, y_label


def make_customer_clusters(axes):
    rng = np.random.default_rng(2)

    def cluster_dots(cx, cy, color, n=7, spread=0.9):
        dots = VGroup()
        for _ in range(n):
            x = float(np.clip(cx + rng.normal(0, spread), 0.4, 9.6))
            y = float(np.clip(cy + rng.normal(0, spread), 0.4, 9.6))
            dots.add(Dot(axes.coords_to_point(x, y), color=color, radius=0.08))
        return dots

    group_a = cluster_dots(2.5, 7.5, BRAND_LOYALIST_COLOR)
    group_b = cluster_dots(8, 2.2, BUDGET_CONSTRAINED_COLOR)
    group_c = cluster_dots(8, 5.8, PRICE_SENSITIVE_COLOR)
    return group_a, group_b, group_c


def encircle(group, color):
    return SurroundingRectangle(group, color=color, buff=0.25, corner_radius=0.4)


# ----------------------------------------------------------------------
# Shared 12-point layout (3 natural groups of 4) for the hierarchical
# clustering / K-Means / evaluation scenes (9-16) -- all agree on the same
# underlying data so callbacks ("the same points as before") are literal.
# Chosen so single-linkage cleanly recovers 3 groups with a large gap
# before the next merge, AND K-Means from KMEANS_INIT_IDX takes several
# real rounds (not just one correction) to converge.
# ----------------------------------------------------------------------
CLUSTER_POINTS_2D = [
    (-4.6, 1.4), (-3.9, 1.6), (-4.5, 0.5), (-3.7, 0.7),
    (-0.4, -1.0), (0.5, -1.6), (0.3, -0.6), (-0.2, -1.7),
    (3.8, 1.2), (4.6, 1.1), (4.0, 0.3), (4.7, 0.5),
]
NATURAL_GROUPS = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]

KMEANS_COLOR_1 = RED
KMEANS_COLOR_2 = GREEN
KMEANS_COLOR_3 = YELLOW
KMEANS_COLORS = [KMEANS_COLOR_1, KMEANS_COLOR_2, KMEANS_COLOR_3]

# All 3 initial centers happen to land in the same natural group -- this
# takes 3 real rounds of reassignment (not just 1) before K-Means converges,
# giving the "moving process" several genuine steps to animate.
KMEANS_INIT_IDX = [0, 1, 2]


def make_cluster_points():
    """The shared 12-point layout as plain (x, y, 0) numpy arrays, in scene
    (not axes-mapped) coordinates."""
    return [np.array([x, y, 0.0]) for x, y in CLUSTER_POINTS_2D]


def compute_dendrogram():
    """Single-linkage hierarchical clustering over CLUSTER_POINTS_2D.

    Returns (Z, icoord, dcoord) where Z is scipy's linkage matrix (one row
    per merge, in merge order) and icoord/dcoord are dendrogram line-segment
    coordinates (leaves spaced 10 apart on x; merge height on y), one
    [x1,x2,x3,x4]/[y1,y2,y3,y4] "step" per row -- guaranteed same order as Z.

    icoord/dcoord are computed here rather than taken from scipy's own
    dendrogram(...)['icoord']/['dcoord']: scipy reorders those internally
    (verified empirically -- e.g. its icoord[0] does not generally
    correspond to Z[0]), which silently desynced the drawn dendrogram shape
    from the merge/color animation driven by Z. Only the leaf ordering
    (chosen to avoid crossing branches) is taken from scipy; the actual
    coordinates are derived directly from Z, index-for-index.
    """
    from scipy.cluster.hierarchy import dendrogram, linkage

    pts = np.array(CLUSTER_POINTS_2D)
    Z = linkage(pts, method="single")
    leaves_order = dendrogram(Z, no_plot=True)["leaves"]

    n = len(Z) + 1
    node_x = {leaf: 10 * rank + 5 for rank, leaf in enumerate(leaves_order)}
    node_height = {i: 0.0 for i in range(n)}
    icoord, dcoord = [], []
    for i, row in enumerate(Z):
        c1, c2 = int(row[0]), int(row[1])
        height = row[2]
        x1, x2 = node_x[c1], node_x[c2]
        h1, h2 = node_height[c1], node_height[c2]
        icoord.append([x1, x1, x2, x2])
        dcoord.append([h1, height, height, h2])
        new_id = n + i
        node_x[new_id] = (x1 + x2) / 2
        node_height[new_id] = height
    return Z, icoord, dcoord


HIER_COLOR_1 = PURPLE
HIER_COLOR_2 = TEAL
HIER_COLOR_3 = MAROON
HIER_COLORS = [HIER_COLOR_1, HIER_COLOR_2, HIER_COLOR_3]


def dendrogram_group_trunk_x(Z, icoord):
    """For each group in NATURAL_GROUPS, the (merge_row_index, trunk_x) of
    the merge that completes it -- trunk_x is in scipy's icoord space and is
    where that group's single branch sits until it next merges. Used to draw
    a "cut at 3 clusters" marker at the right x-positions."""
    n = len(Z) + 1
    members = {i: [i] for i in range(n)}
    result = {}
    for i, row in enumerate(Z):
        c1, c2 = int(row[0]), int(row[1])
        merged = sorted(members[c1] + members[c2])
        members[n + i] = merged
        trunk_x = (icoord[i][0] + icoord[i][3]) / 2
        for g in NATURAL_GROUPS:
            if merged == sorted(g):
                result[tuple(g)] = (i, trunk_x)
    return result


def dendrogram_cut_height(Z, icoord):
    """The merge height (scipy dcoord space) exactly between the last merge
    that completes one of the 3 natural groups and the next merge after it
    -- i.e. a height at which cutting the dendrogram yields NATURAL_GROUPS."""
    trunks = dendrogram_group_trunk_x(Z, icoord)
    last_row = max(row for row, _ in trunks.values())
    below = Z[last_row][2]
    above = Z[last_row + 1][2]
    return (below + above) / 2, trunks


def dendrogram_merge_members(Z):
    """For each merge row in Z, the two lists of original point indices
    being merged at that step, e.g. [([0], [2]), ([1], [0, 2]), ...]."""
    n = len(Z) + 1
    members = {i: [i] for i in range(n)}
    result = []
    for i, row in enumerate(Z):
        c1, c2 = int(row[0]), int(row[1])
        left, right = members[c1], members[c2]
        result.append((left, right))
        members[n + i] = left + right
    return result


def kmeans_iterations(max_rounds=8):
    """Lloyd's algorithm (assign -> recompute centroids) over
    make_cluster_points(), starting from KMEANS_INIT_IDX, run until the
    assignment stops changing (confirmed by one extra round). Deterministic.

    Returns a list of (centers, assignment) tuples -- for the current data
    this is 4 rounds: an initial bad assignment, two real correction
    rounds, then one round confirming convergence (same assignment as the
    round before). centers is a (3,2) array; assignment is a length-N array
    of cluster indices (0/1/2) matching KMEANS_COLORS, in the same point
    order as make_cluster_points().
    """
    pts = np.array(CLUSTER_POINTS_2D)
    centers = pts[KMEANS_INIT_IDX].copy().astype(float)
    steps = []
    prev_assign = None
    for _ in range(max_rounds):
        d = np.linalg.norm(pts[:, None, :] - centers[None, :, :], axis=2)
        assign = d.argmin(axis=1)
        steps.append((centers.copy(), assign.copy()))
        if prev_assign is not None and np.array_equal(assign, prev_assign):
            break
        prev_assign = assign.copy()
        centers = np.array(
            [
                pts[assign == k].mean(axis=0) if (assign == k).any() else centers[k]
                for k in range(3)
            ]
        )
    return steps


def kmeans_final_centroids():
    """Fully-converged K-Means centroids, consistent with their assignment.

    kmeans_iterations()'s last step pairs an assignment with the centroids
    that *produced* it (one round behind), which is exactly what scene_11
    wants to narrate -- but scene_14's SSE/Silhouette need a centroid that
    truly is the mean of its own cluster's points, so this recomputes once
    more from the (already-stable) final assignment.
    """
    pts = np.array(CLUSTER_POINTS_2D)
    _, assign = kmeans_iterations()[-1]
    centers = np.array([pts[assign == k].mean(axis=0) for k in range(3)])
    return centers, assign


def make_mini_dendrogram(width=2.2, height=1.5, color=WHITE):
    """A small complete dendrogram (all merges, from compute_dendrogram())
    scaled to fit within width x height, centered on the origin. Used by
    scene_09 (taxonomy) and scene_12 (recalling "in hierarchical
    clustering...") -- a real dendrogram of the shared data, not a glyph."""
    Z, icoord, dcoord = compute_dendrogram()
    icoord = np.array(icoord)
    dcoord = np.array(dcoord)
    x_mid = (icoord.min() + icoord.max()) / 2
    x_span = icoord.max() - icoord.min()
    y_span = dcoord.max() - dcoord.min()

    def mapper(x, y):
        nx = (x - x_mid) / x_span * width
        ny = y / y_span * height - height / 2
        return np.array([nx, ny, 0])

    group = VGroup()
    for i in range(len(Z)):
        pts = [mapper(x, y) for x, y in zip(icoord[i], dcoord[i])]
        u = VMobject(color=color, stroke_width=1.75)
        u.set_points_as_corners(pts)
        group.add(u)
    return group


def make_mini_kmeans_scatter(width=2.2, height=1.5, dot_radius=0.045):
    """A small scatter of the shared data, colored by its actual converged
    K-Means assignment (kmeans_final_centroids()), scaled to fit within
    width x height, centered on the origin. Used by scene_09 (taxonomy) and
    scene_12 -- a real K-Means result, not a glyph."""
    pts = np.array(CLUSTER_POINTS_2D)
    _, assign = kmeans_final_centroids()
    x_mid = (pts[:, 0].min() + pts[:, 0].max()) / 2
    y_mid = (pts[:, 1].min() + pts[:, 1].max()) / 2
    x_span = pts[:, 0].max() - pts[:, 0].min()
    y_span = pts[:, 1].max() - pts[:, 1].min()

    def mapper(x, y):
        nx = (x - x_mid) / x_span * width
        ny = (y - y_mid) / y_span * height
        return np.array([nx, ny, 0])

    return VGroup(
        *[
            Dot(mapper(x, y), radius=dot_radius, color=KMEANS_COLORS[assign[i]])
            for i, (x, y) in enumerate(pts)
        ]
    )
