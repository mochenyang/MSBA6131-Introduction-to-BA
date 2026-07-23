# Scene 1

**Text**: This video will discuss cluster analysis.
**Visual**: plain text display in the center

# Scene 2

**Text**: Imagine you are a data scientist working for Walmart, and you want to understand if Walmart's 280 million customers fall into any distinct groups. This is known as "market segmentation", and is a common exercise to understand a one's customer base. For concreteness, say you describe each customer based on their shopping budget -- how much money they want to spend shopping at Walmart -- and price sensitivity -- how sensitive they are with respect to price changes. Looking at this plot, we can eyeball at least three distinct groups, or "clusters", of customesr. One group has a relatively high budget and low price sensitivity. They are willing and are able to spend more money if needed, perhaps because they are loyal to certain brands. A second group has relatively low budget and high sensitivity. Because they don't have a big budget, they may stop buying certain things if the price increase. A third group has comparatively higher budget than the second group, but similarly high price sensitivity. These are people who are very careful with their money.

Having such information can help executives at Walmart customize their marketing strategy to customers of each group. For the brand loyalist, brand promotions campaigns may get them to spend more money. For the budget constrained customers, advertising low-price options can be a good way to keep their businesses. For the price sensitive shoppers, sending them discount coupons can meaningfully boost spending.

**Visual**: a 2D scatter plot representing some hypothetical customers that fall into three clusters as indicated in the text. Respectively highlighting each cluster.

# Scene 3

**Text**: Market segmentation is a representative application of cluster analysis. Formally, the goal of clustering analysis is to organize data points, or objects in general, into homogeneous and hopefully meaningful groups. Each group is called a cluster.

There are two objectives of clustering. First, we want data points that belong to the same cluster to be similar to each other -- this is called high intra-similarity. Second, we want data points that belong to different clusters to be different from each other -- this is called low inter-similarity. In general, high intra-similarity and low inter-similarity together indicate that we have discovered natural grouping structures in the data: each group is sufficiently homogeneous, and different groups are sufficiently separated.

**Visual**: show a cloud of scattered points organizing into 2-3 colored clusters. Circle each cluster and add an inward-pointing arrow labeled "high intra-similarity" within one cluster, and an outward double-arrow labeled "low inter-similarity" between two clusters.

# Scene 4

**Text**: Clustering analysis, like association rule mining, is a type of exploratory analytics. To make this point clear, it's worth differentiating clustering from classification, or categorization, which is a predictive analytics topic we'll discuss later. The difference is that clustering aims to discover groups from data, whereas classification aims to put data into pre-defined groups.

Take the Walmart market segmentation case as an example. Before conducting the analysis, Walmart does not know there would be three groups of customers -- the three groups are a result of the segmentation analysis. In a predictive classification task, by contrast, the groups (also called classes) must be pre-specified. For example, classifying social media posts as having positive or negative sentiment is classification, because the positive and negative groups are pre-specified.

**Visual**: split-screen comparison. Left side titled "Clustering (Exploratory)": unlabeled scattered points animate into discovered, newly-colored groups. Right side titled "Classification (Predictive)": points move into two pre-labeled bins, "Positive" and "Negative", that are already drawn before the points arrive.

# Scene 5

**Text**: What can we use clustering for? Broadly speaking, clustering can help us understand and summarize the structure of our data, as well as achieve customization. Successful clustering analysis can help us gain a deeper understanding of the distinct groups and patterns in our data, and allows us to study the data by examining groups rather than individual data points. In addition, businesses can design customized strategies for each group that cater to their specific characteristics.

**Visual**: two icon-labeled panels appear side by side. Left panel, "Understand & Summarize Structure": many small dots collapse into a few labeled group icons. Right panel, "Customization": each group icon connects to a distinct tailored-strategy icon (e.g., a coupon, a loyalty badge, an ad).

# Scene 6

**Text**: So, how do we conduct clustering analysis? Let's first lay out the ingredients we need.

If the dataset has low dimensions -- in other words, a small number of variables describing each data point -- clustering can be as simple as plotting the data and visually identifying clusters. In general, however, once there are more than three variables in the dataset, we need a systematic approach to clustering. First, we need to be able to measure the similarity between data points, because we want to put similar data points in the same cluster and dissimilar ones in different clusters. Second, we need to measure the similarity between clusters, which tells us how well-separated different clusters are. We also need a way of choosing the number of clusters and evaluating the quality of a clustering solution, so that we can identify the best one. Finally, we need to be able to interpret clustering results and make sense of each cluster.

**Visual**: a checklist/roadmap graphic with five items that appear one at a time as they're mentioned: (1) Measure similarity between data points, (2) Measure similarity between clusters, (3) Choose the number of clusters, (4) Evaluate solution quality, (5) Interpret results.

# Scene 7

**Text**: In this video, we are going to look at how to measure similarity between data points and between clusters, which is a pre-requisite to implementing any clustering algorithm. Note that I'll use the words "similarity" and "distance" interchangeably -- greater distance means less similarity, and vice versa.

Defining proper distance metrics is often the first step of running any clustering algorithm. There are a number of distance metrics available, and picking the appropriate one depends jointly on the type of your data and on the particular application.

**Visual**: title card "Measuring Distance". Show two abstract points A and B with a dashed connecting line labeled alternately "distance" and "similarity" (crossfade between the two labels to emphasize they're inverses).

# Scene 8

**Text**: In the following discussion, I'll consider the problem of measuring the distance between two data points, A and B, each characterized by a vector of k attributes, or features.

If your data is numeric or continuous, there are a few choices of distance metrics. First, Euclidean distance simply measures the straight-line distance between A and B -- it's perhaps the most common choice. Second, Manhattan distance is calculated as the sum of absolute differences across all features. To understand this metric, imagine A and B are placed on a grid, and you want to travel from A to B: you can only move along the grid, horizontally or vertically, but not diagonally. The distance you'd need to travel is the Manhattan distance. The third metric, max-coordinate distance, is the largest difference among all features. Compared to Euclidean and Manhattan distance, it's used less often -- you can follow the Wikipedia link in the slide to see some specific application domains where it may be appropriate.

**Visual**: show points A and B, each labeled as a vector of k features. Then show three side-by-side diagrams on a 2D grid with the same A and B: (1) a straight diagonal line labeled "Euclidean Distance" with its formula, (2) a stair-step path along grid lines labeled "Manhattan Distance" with its formula, (3) the single longest-axis segment highlighted, labeled "Max-Coordinate Distance" with its formula.

# Scene 9

**Text**: To see how to calculate these three distances, consider a simple example where A and B are each described by three attributes. First, we calculate the absolute difference between A and B on each attribute: 2, 3, and 5. Then, Euclidean distance is the square root of the sum of the squared differences, which is the square root of 38. Manhattan distance is the sum of the absolute differences, which is 10. And max-coordinate distance is the maximum of the absolute differences, which is 5.

**Visual**: a small table showing A's and B's values across 3 attributes, with a row below showing the absolute differences (2, 3, 5). Below the table, three formulas compute in sequence, each highlighting as it's mentioned: sqrt(2^2+3^2+5^2) = sqrt(38); |2|+|3|+|5| = 10; max(2,3,5) = 5.

# Scene 10

**Text**: If the data is categorical, and in particular if all attributes are binary, you can consider using matching distance or Jaccard distance. Under matching distance, the distance between A and B is simply the fraction of attributes on which A and B have different values -- the number of attributes on which A and B mismatch, divided by the total number of attributes. Jaccard distance is almost the same as matching distance, except for a small difference in the denominator: instead of counting all attributes, Jaccard distance excludes the attributes where both A and B take the value 0.

**Visual**: show the matching distance formula: (# mismatches) / (total attributes). Below it, show the Jaccard distance formula: (# mismatches) / (total attributes - # of 0-0 matches), with the excluded 0-0 term visually crossed out or grayed to highlight the difference from matching distance.

# Scene 11

**Text**: Before I explain why we do this, let's first look at an example. Suppose we want to measure the similarity between customers A and B based on what they buy, in the sense that people who buy similar stuff should be considered similar. Consider a shop that sells four products -- coffee, tea, cookie, and bagel -- and two customers, A and B, whose shopping history is represented by a binary vector. For instance, customer A, who purchased coffee and bagel, can be represented as the vector 1, 0, 0, 1.

We can see that A and B mismatch on coffee and tea -- one person bought the product but the other didn't. These two products characterize the difference between A and B. So the matching distance between A and B is 2 (the number of mismatches) divided by 4 (the total number of attributes). The Jaccard distance, in contrast, is 2 over 3, because we exclude "cookie", where neither A nor B made a purchase.

**Visual**: a table with columns Coffee, Tea, Cookie, Bagel and rows for Customer A (1,0,0,1) and Customer B. Highlight mismatched columns (coffee, tea) in one color and the shared 0-0 column (cookie) in a different, grayed-out color. Show the matching distance calculation (2/4) and Jaccard distance calculation (2/3) below, with the grayed-out cookie column visibly excluded from the Jaccard denominator.

# Scene 12

**Text**: Now, to understand the difference between matching distance and Jaccard distance, and why it matters, think about a typical supermarket shopping scenario. A typical supermarket sells thousands of products, and each customer usually only buys a handful of them, so each customer's shopping-history vector will have a lot of 0s and relatively few 1s. Under matching distance, any two arbitrary customers would seem very similar to each other, simply because there are thousands of products neither of them purchased. But in a supermarket context, it's really the handful of things people do buy that characterizes who they are -- not the thousands of things they don't buy.

Jaccard distance solves this asymmetry by ignoring 0-0 matches. Formally, Jaccard distance is appropriate for what's known as asymmetric binary data, where a 0-0 match is not as meaningful as a 1-1 match. By excluding 0-0 matches, Jaccard distance makes sure the calculation isn't distorted. Matching distance, in contrast, is appropriate for cases where both 0-0 and 1-1 matches are equally meaningful.

**Visual**: show a long binary vector (e.g., 20+ products) for two customers, mostly 0s with a few scattered 1s. Zoom out to emphasize how many 0-0 matches dominate the vector. Then show a side-by-side comparison: "Matching Distance" with a near-zero value (customers appear falsely similar) versus "Jaccard Distance" with a much higher, more meaningful value, after the 0-0 matches are grayed out and excluded.

# Scene 13

**Text**: Another very important topic when calculating distances between data points is normalization. If two attributes of your data take values from very different ranges, the attribute with the wider range can distort the distance calculation. Consider two common attributes: age and income. Age takes values from a small range, say 0 to 100, whereas income takes values from a much wider range, from thousands to millions or more. When calculating the distance between two individuals based on age and income, the difference in income, simply by virtue of its wider range, will dominate the calculation and render the difference in age too small to matter.

Normalization is a simple technique to solve this issue, by rescaling each attribute so that they fall into the same range. A common method is min-max normalization: for each attribute, find the max and min values, and rescale any value x to (x - min) / (max - min). This ensures the normalized value always falls within [0, 1].

**Visual**: show two number lines side by side: one for Age (0-100) and one for Income ($0-$1,000,000+), with the income line dramatically wider. Show a distance calculation where the income term visually dwarfs the age term. Then animate the min-max normalization formula rescaling both number lines to a common [0,1] range, after which the two terms become comparably sized.

# Scene 14

**Text**: So far we've talked about how to measure the distance between data points. We also need to know how to measure the distance between clusters. Fortunately, distance between clusters is basically defined by selecting or aggregating certain distances between the data points in each cluster. In this and the next scene, you'll see six different ways of measuring distance between clusters.

Single linkage measures the distance between two clusters as the shortest distance between one data point in each cluster, and complete linkage instead looks at the longest such distance. Average linkage measures all pairwise distances between data points in the two clusters and takes the average.

**Visual**: show two clusters of points, cluster 1 and cluster 2. Animate three versions: (1) highlight the single closest pair of points across clusters, labeled "Single Linkage"; (2) highlight the single farthest pair, labeled "Complete Linkage"; (3) draw all pairwise connecting lines between the two clusters and show them averaging into one value, labeled "Average Linkage".

# Scene 15

**Text**: Centroid distance measures the distance between the centroid of each cluster, which is the geometric center of a cluster. Finally, average group linkage and Ward's method both first imagine that the two clusters are merged into a single, bigger cluster. Average group linkage measures the average pairwise distance between all data points in that merged cluster, whereas Ward's method measures the sum of squared distances between each data point and the centroid of the merged cluster.

In practice, there's often not much prior preference for which measure to use. You can repeat the clustering analysis with different measures, and if the key results are similar, that shows the robustness of your conclusions.

**Visual**: show the same two clusters with their centroids marked as X's; draw a line between the centroids labeled "Centroid Distance". Then animate the two clusters merging into one combined cluster: for "Average Group Linkage", show all pairwise distances within the merged cluster averaging together; for "Ward's Method", show each point connecting to the merged cluster's centroid with squared-distance labels summing up.

# Scene 16

**Text**: In this video, we're going to learn two popular clustering algorithms: hierarchical clustering and K-Means clustering.

There are many clustering methods available. One type is the hierarchical method, where the algorithm forms larger clusters from smaller ones, or breaks larger clusters into smaller ones, in a hierarchical fashion -- we'll talk about a specific technique called hierarchical clustering. Another type is the partition-based method, where the idea is to directly partition the data into K groups, K being the desired number of clusters. K-Means belongs to this category.

**Visual**: title card "Hierarchical Clustering & K-Means". Below it, show a simple taxonomy diagram branching into two boxes: "Hierarchical Methods" (icon of a tree/dendrogram) and "Partition-Based Methods" (icon of data split directly into K labeled boxes), with "Hierarchical Clustering" and "K-Means" labeled underneath each respectively.

# Scene 17

**Text**: Let's start with hierarchical clustering, which can be understood intuitively. The idea is to take a bottom-up approach: starting from individual data points or smaller clusters, we form larger clusters in a hierarchical manner.

More specifically, in step 1, we assign each data point to be its own cluster. In step 2, we merge the two clusters that are closest to each other, based on a choice of distance metric, so that a larger cluster is formed. We then simply repeat step 2, each time merging the two closest clusters into a larger one, until there is only one cluster left containing all the data points.

The input to hierarchical clustering is typically a distance matrix, which records the pairwise distances between all data points -- this makes it easy to find the closest data points or clusters at each step.

**Visual**: animate a set of ~7 scattered points, each starting as its own single-point cluster (step 1). Step by step, merge the two closest clusters together (highlighting the pair before merging), repeating until all points form one big cluster. Alongside, show a small distance matrix table that's referenced/highlighted at each merge step.

# Scene 18

**Text**: More important, we need to understand the output of the hierarchical clustering algorithm, which is a graph called a dendrogram. The dendrogram records the entire cluster-merging process, and therefore contains solutions for any number of clusters you may want.

To read a dendrogram, imagine it as a tree with many branches that you want to cut to read out a clustering solution. Take the following dendrogram as an example: it shows the merging process of 7 data points, which start out as their own clusters and end up in a single cluster. If I want the 2-cluster solution, I'd cut the tree vertically with a line positioned so it intersects the tree exactly 2 times. As a result, two branches fall off -- one cluster containing data points A, B, C, D, and the other containing E, F, G. If instead I want the 4-cluster solution, I'd cut the tree exactly 4 times, giving me AB as a cluster, CD as a cluster, E as a cluster, and FG as a cluster.

**Visual**: show a full dendrogram for 7 labeled data points (A-G) built from the merges in the previous scene, branches rising to a single root. Animate a horizontal red cutting line sliding down: pause where it crosses 2 branches, highlighting the resulting {A,B,C,D} and {E,F,G} clusters in two colors. Then slide the line to cross 4 branches, highlighting {A,B}, {C,D}, {E}, {F,G} in four colors.

# Scene 19

**Text**: Now let's move on to K-Means, which is a completely different approach. The idea of K-Means is to directly partition the data into K clusters, then make incremental adjustments to improve the partition.

Users specify K, the number of clusters, in advance. In step 1, you choose K data points at random to be the centers of the K clusters. In step 2, you assign the remaining data points to the closest cluster center -- at the end of this step, you already have K clusters. In step 3, you find the new centroids of the K clusters, and repeat steps 2 and 3 until the cluster assignments no longer change.

**Visual**: show a numbered 3-step flowchart: Step 1 "Pick K random points as initial centers", Step 2 "Assign each point to its closest center", Step 3 "Recompute centroids", with a looping arrow from Step 3 back to Step 2 labeled "repeat until assignments stop changing".

# Scene 20

**Text**: If the above description is a bit too abstract, here's a graphical illustration. Suppose we want to find 2 clusters in this data. We start by randomly choosing 2 data points, colored red and green, and pretend they're the centers of the two clusters. Next, we assign each remaining data point to either the red or green cluster, whichever is closer. Since we chose the two initial points at random, the result at the end of this step doesn't look very good.

But we don't need to worry, because we'll next find the new centroids of the red and green clusters and re-assign all data points to the two clusters. Comparing this step to the previous one, you can already see the red cluster gaining territory and the green cluster retreating to the bottom right corner. We repeat this process multiple times until the red and green clusters no longer change. In practice, because K-Means results can be sensitive to the random initial points chosen, it's common to run the algorithm multiple times with different random initializations, to get more stable results.

**Visual**: a 4-panel animated sequence on the same scatter plot: Panel 1, two random points highlighted red and green as initial centers. Panel 2, all points colored red or green based on nearest center (messy-looking split). Panel 3, centroids recompute (shown moving) and points re-colored -- red cluster visibly gains territory. Panel 4, after further iterations, the clusters stabilize into two clean, well-separated groups.

# Scene 21

**Text**: In this video, I'll talk about how to interpret clustering results and evaluate the quality of a clustering solution.

Recall that the purpose of clustering is to put data points into homogeneous groups, such that points in each group are similar to each other. Consistent with this, we can interpret each cluster by its "average" data point, which is the centroid of the cluster -- formally, the mean of all data points in that cluster. It may or may not be an actual data point itself, but it nonetheless represents the average characteristics of the data in that cluster.

More importantly, given the exploratory nature of clustering analysis, interpreting clustering results must be combined with domain knowledge. Think about whether the clusters make sense to you as a data scientist, and whether they help you solve the problem you set out to answer. Instead of trying to find the objectively best solution, keep in mind that there is no absolute "correct" clustering result -- your interpretation and evaluation depend on your business problem and goals.

**Visual**: show a cluster of scattered points with its centroid marked as a large X at the average position. Label the centroid "Cluster Profile". Then show a thought-bubble or checklist next to it: "Does this make sense given what I know about the business?" to emphasize the domain-knowledge step.

# Scene 22

**Text**: There are a few metrics we can use to quantify the quality of a clustering solution. Remember, ideally we want clusters to have high intra-similarity, or cohesion, and low inter-similarity, or separation. If we can quantitatively measure cohesion and separation, we can measure the quality of a clustering solution.

The first metric, sum-of-squared-errors, or SSE, measures cohesion. Suppose you have K clusters, C1 through Ck, with centroids m1 through mk. For a data point X, we define the error of X as the distance between X and its cluster's centroid. SSE is then the sum of squared errors across all data points. A lower SSE means data points are generally close to their cluster centers, indicating high cohesion. However, SSE doesn't tell us about separation -- for that, we need a different metric.

**Visual**: show several clusters with their centroids marked. For one data point X, draw a line to its centroid labeled "error". Show the SSE formula building up: SSE = sum over all clusters and points of (distance from X to its centroid)^2. Animate the formula's value shrinking as points move closer to their centroids, to illustrate "lower SSE = higher cohesion".

# Scene 23

**Text**: The metric that captures both cohesion and separation is the Silhouette coefficient. Given a data point X in cluster C, we define two quantities. A(x) measures the average distance between X and other data points in the same cluster C -- a measure of cohesion, where a smaller A(x) indicates a tighter, more cohesive cluster. B(x) measures the smallest average distance between X and all data points in another cluster -- it captures how close X is to its nearest neighboring cluster; a larger B(x) means X is well separated from other clusters.

The Silhouette coefficient of X is then calculated from A(x) and B(x). We can aggregate the Silhouette coefficients of all points in a cluster to reflect that cluster's quality, or average across all points to capture the quality of the entire clustering solution. A higher Silhouette coefficient implies B(x) is higher, A(x) is lower, or both -- meaning the clustering solution has both high cohesion and good separation.

**Visual**: show a data point X inside cluster C, with two elements: a set of short arrows to other points in the same cluster C labeled "A(x): avg. distance within cluster" and a set of arrows to the nearest neighboring cluster labeled "B(x): avg. distance to nearest cluster". Display the Silhouette coefficient formula combining A(x) and B(x), with a scale below showing low-to-high values corresponding to poor-to-good clustering.

# Scene 24

**Text**: The final topic in clustering is how to choose the proper number of clusters. If we're using K-Means, we need to specify a cluster number to begin with. Even with hierarchical clustering, we still need to figure out a reasonable cluster number afterward.

The first method is to examine the dendrogram and look for large gaps. Take the following dendrogram as an example: after three clusters form during the merging process, there's a large gap before two of those three clusters merge into a bigger one. This is good evidence that there are 3 natural clusters in the data, because going from 3 clusters to 2 means merging clusters that are very far apart.

**Visual**: show a dendrogram where the merge heights are drawn to scale. Highlight the point where 3 clusters have formed, then visually emphasize the unusually large vertical gap before the next merge (e.g., with a bracket and callout labeled "large gap = 3 natural clusters").

# Scene 25

**Text**: Another method for picking the number of clusters, usable with both K-Means and hierarchical clustering, is to try different numbers of clusters and plot the SSE measure against the number of clusters. The goal is to look for an "elbow" shape in the SSE plot -- a point where SSE drops sharply before, then becomes fairly flat after. Because SSE tends to drop as we increase the number of clusters, hitting an elbow point typically means we've found a natural number of clusters. Take the graph as an example: finding the elbow point correctly tells you there are 10 clusters in the data.

Finally, I'd like to remind you that although these methods are useful in practice, the ultimate judge for choosing the number of clusters is whether the clustering solution is meaningful and useful for solving your data analytics problem.

**Visual**: show a line plot with number of clusters (K) on the x-axis and SSE on the y-axis, sharply decreasing then flattening out. Animate a callout circling the "elbow" at K=10, with a dashed vertical line dropping to the x-axis. End on a text callout: "The best K is the one that's meaningful for your problem."
