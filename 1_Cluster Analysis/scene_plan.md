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

**Visual**: show definition of clustering in plain text. Then show the same scatter plot as in scene 2 with the same clusters. Circle each cluster and add an inward-pointing arrow labeled "high intra-similarity" within one cluster, and an outward double-arrow labeled "low inter-similarity" between two clusters.

# Scene 4

**Text**: Clustering analysis, like association rule mining, is a type of exploratory analytics. To make this point clear, it's worth differentiating clustering from classification, which is a predictive analytics topic we'll discuss later. The difference is that clustering aims to discover groups from data, whereas classification aims to put data into pre-defined groups.

Take the Walmart market segmentation case as an example. Before conducting the analysis, Walmart does not know there would be three groups of customers -- the three groups are a result of the segmentation analysis. In a predictive classification task, by contrast, the groups (also called classes) must be pre-specified. For example, classifying social media posts as having positive or negative sentiment is classification, because the positive and negative groups are pre-specified.

**Visual**: split-screen comparison. Left side titled "Clustering (Exploratory)": unlabeled scattered points animate into discovered, newly-colored groups. Right side titled "Classification (Predictive)": social media posts move into two pre-labeled bins, "Positive" and "Negative", that are already drawn before the points arrive.

# Scene 5

**Text**: So, how do we conduct clustering analysis? Let's first lay out the ingredients we need.

If the dataset has low dimensions -- in other words, a small number of variables describing each data point -- clustering can be as simple as plotting the data and visually identifying clusters. In general, however, once there are more than three variables in the dataset, we need a systematic approach to clustering. First, we need to be able to measure the similarity between data points, because we want to put similar data points in the same cluster and dissimilar ones in different clusters. Second, we need a way of choosing the number of clusters and evaluating the quality of a clustering solution, so that we can identify the best one. Finally, we need to be able to interpret clustering results and make sense of each cluster.

**Visual**: a checklist/roadmap graphic with five items that appear one at a time as they're mentioned: (1) Measure similarity between data points, (2) Choose the number of clusters and Evaluate solution quality, (4) Interpret results.

# Scene 6

**Text**: Defining proper distance metrics is often the first step of running any clustering algorithm. There are a number of distance metrics available, and picking the appropriate one depends jointly on the type of your data and on the particular application.

Let's consider the problem of measuring the distance between two data points, A and B, each characterized by a vector of k attributes, or features.

If your data is numeric or continuous, there are a few choices of distance metrics. First, Euclidean distance simply measures the straight-line distance between A and B -- it's perhaps the most common choice. Second, Manhattan distance is calculated as the sum of absolute differences across all features. To understand this metric, imagine A and B are placed on a grid, and you want to travel from A to B: you can only move along the grid, horizontally or vertically, but not diagonally. The distance you'd need to travel is the Manhattan distance. The third metric, max-coordinate distance, is the largest difference among all features. Compared to Euclidean and Manhattan distance, it's used less often.

If the data is categorical, and in particular if all attributes are binary, you can consider using matching distance or Jaccard distance. Under matching distance, the distance between A and B is simply the fraction of attributes on which A and B have different values -- the number of attributes on which A and B mismatch, divided by the total number of attributes. Jaccard distance is almost the same as matching distance, except for a small difference in the denominator: instead of counting all attributes, Jaccard distance excludes the attributes where both A and B take the value 0. The reason to do so is that, in many real-world scenarios, a 0-0 match is less informative than a 1-1 match about two data points' similarity. Think about a typical supermarket shopping scenario. A typical supermarket sells thousands of products, and each customer usually only buys a handful of them, so each customer's shopping-history vector will have a lot of 0s and relatively few 1s. Under matching distance, any two arbitrary customers would seem very similar to each other, simply because there are thousands of products neither of them purchased. But in a supermarket context, it's really the handful of things people do buy that characterizes who they are -- not the thousands of things they don't buy. Jaccard distance solves this asymmetry by ignoring 0-0 matches. Formally, Jaccard distance is appropriate for what's known as asymmetric binary data, where a 0-0 match is not as meaningful as a 1-1 match. By excluding 0-0 matches, Jaccard distance makes sure the calculation isn't distorted. 

**Visual**: split-screen layout. On the left side, show bullet points of each distance metric. On the right hand side, show visualization of how the distance is measured. Specifically, under the numerical feature case, show points A and B on a 2D grid and : (1) a straight diagonal line labeled "Euclidean Distance" with its formula, (2) a stair-step path along grid lines labeled "Manhattan Distance" with its formula, (3) the single longest-axis segment highlighted, labeled "Max-Coordinate Distance" with its formula. Under binary case, simply show A and B each as a vector of 0s and 1s and show calculations of the distance metrics. 

# Scene 7

**Text**: Another very important topic when calculating distances between data points is normalization. If two attributes of your data take values from very different ranges, the attribute with the wider range can distort the distance calculation. Consider two common attributes: age and income. Age takes values from a small range, say 0 to 100, whereas income takes values from a much wider range, from thousands to millions or more. When calculating the distance between two individuals based on age and income, the difference in income, simply by virtue of its wider range, will dominate the calculation and render the difference in age too small to matter.

Normalization is a simple technique to solve this issue, by rescaling each attribute so that they fall into the same range. A common method is min-max normalization: for each attribute, find the max and min values, and rescale any value x to (x - min) / (max - min). This ensures the normalized value always falls within [0, 1].

**Visual**: show two number lines side by side: one for Age (0-100) and one for Income ($0-$1,000,000+), with the income line dramatically wider. Show a distance calculation where the income term visually dwarfs the age term. Then animate the min-max normalization formula rescaling both number lines to a common [0,1] range, after which the two terms become comparably sized.

# Scene 8

**Text**: So far we've talked about how to measure the distance between data points. We also need to know how to measure the distance between clusters. Fortunately, distance between clusters is basically defined by selecting or aggregating certain distances between the data points in each cluster. Here are some commonly used metrics.

Single linkage measures the distance between two clusters as the shortest distance between one data point in each cluster, and complete linkage instead looks at the longest such distance. Average linkage measures all pairwise distances between data points in the two clusters and takes the average. Centroid distance measures the distance between the centroid of each cluster, which is the geometric center of a cluster. Finally, average group linkage and Ward's method both first imagine that the two clusters are merged into a single, bigger cluster. Average group linkage measures the average pairwise distance between all data points in that merged cluster, whereas Ward's method measures the sum of squared distances between each data point and the centroid of the merged cluster.

**Visual**: show two clusters of points, cluster 1 and cluster 2. Animate three versions: (1) highlight the single closest pair of points across clusters, labeled "Single Linkage"; (2) highlight the single farthest pair, labeled "Complete Linkage"; (3) draw all pairwise connecting lines between the two clusters and show them averaging into one value, labeled "Average Linkage". Next, with their centroids marked as X's; draw a line between the centroids labeled "Centroid Distance". Then animate the two clusters merging into one combined cluster: for "Average Group Linkage", show all pairwise distances within the merged cluster averaging together; for "Ward's Method", show each point connecting to the merged cluster's centroid with squared-distance labels summing up.

# Scene 9

**Text**: We now have all the ingredients needed for doing clustering analyses. There are many different types of clustering methods. One type is the hierarchical method, where the algorithm forms larger clusters from smaller ones, or breaks larger clusters into smaller ones, in a hierarchical fashion -- we'll talk about a specific technique called hierarchical clustering. Another type is the partition-based method, where the idea is to directly partition the data into K groups, K being the desired number of clusters. K-Means belongs to this category.

**Visual**: title card "Clustering Methods". Below it, show a simple taxonomy diagram branching into two boxes: "Hierarchical Methods" (icon of a tree/dendrogram) and "Partition-Based Methods" (icon of data split directly into K labeled boxes), with "Hierarchical Clustering" and "K-Means" labeled underneath each respectively.

# Scene 10

**Text**: Let's start with hierarchical clustering, which can be understood intuitively. The idea is to take a bottom-up approach: starting from individual data points or smaller clusters, we form larger clusters in a hierarchical manner.

More specifically, in step 1, we assign each data point to be its own cluster. In step 2, we merge the two clusters that are closest to each other, based on our choice of a distance metric, so that a larger cluster is formed. We then simply repeat step 2, each time merging the two closest clusters into a larger one, until there is only one cluster left containing all the data points.

The output of the hierarchical clustering algorithm is a graph called a dendrogram. The dendrogram records the entire cluster-merging process, and therefore contains solutions for any number of clusters you may want. To read a dendrogram, imagine it as a tree with many branches that you want to cut to read out a clustering solution. For example, in this case, if I want a 3-cluster solution, I can cut the dendrogram here, and obtain the data points that belong to each of the three clusters.

**Visual**: animate a set of ~7 scattered points, each starting as its own single-point cluster (step 1). Step by step, merge the two closest clusters together (highlighting the pair before merging), repeating until all points form one big cluster. Next, when the text talks about dendrograms, show the dendrogram growing from root to top as the cluster process progresses. When the text talks about reading a dendrogram, cut it with 3 intersections and highlight the resulting 3-cluster solution.

# Scene 11

**Text**: In comparison, K-Means is a completely different approach. The idea of K-Means is to directly partition the data into K clusters, then make incremental adjustments to improve the partition. Here's an illustration.

Suppose we want to find 3 clusters in this data. We start by randomly choosing 3 data points, colored red, green, and yellow, and pretend they're the centers of the three clusters. Next, we assign each remaining data point to a cluster based on which center it is closest to. Since we chose the three initial points at random, the result at the end of this step doesn't look very good.

No need to worry, because we'll next find the new centroids of each of the three clusters and re-assign all data points to the the three clusters. Comparing this step to the previous one, you can already see some improvements. We repeat this process multiple times until the clusters no longer change.

**Visual**: Take the same ~7 data points used before and animate the 3-cluster k-means process. Use red, green, and yellow to mark the three clusters.

# Scene 12

**Text**: Let's take a pause here. Regardless of which method you are using in practice, you need to determine the number of clusters. In hierarchical clustering, you need to determine the number of clusters to read out the cluster solutions. In k-means, you need to explicitly specify number of clusters as an input to the algorithm. So, how should we determine the number of clusters?

This is fundamentally an evaluation question. Ideally, we want to pick the cluster number that produces the "best" clustering solution. But what is the "best" clustering solution? Remember, we want clusters to have high intra-similarity (meaning that data points in the same clusters are similar to each other). This is known as cohesion. We also want clusters to have low inter-similarity (meaning that different clusters should be well separated from one another). This is known as separation. 

**Visual**: have a title "How to Determine Number of Clusters" with two boxes below it, respectively having "High Intra-Similarity" and "Low Inter-Similarity" as box title. In each box, show the same two clusters of data points and highlight respectively the cohesion and separation aspects.

# Scene 13

**Text**: For hierarchical clustering, the cohesion and separation of clusters can be visually gauged by inspecting the dendrogram. Take the following dendrogram as an example: after three clusters form during the merging process, there's a large gap before two of those three clusters merge into a bigger one. This is good evidence that there are 3 natural clusters in the data, because going from 3 clusters to 2 means merging clusters that are very far apart.

**Visual**: show a dendrogram where the merge heights are drawn to scale. Highlight the point where 3 clusters have formed, then visually emphasize the unusually large vertical gap before the next merge (e.g., with a bracket and callout labeled "large gap = 3 natural clusters").

# Scene 14

**Text**: Besides visual inspection, cohesion and separation can also be quantatively calculated from data. The first metric, sum-of-squared-errors, or SSE, measures cohesion. Suppose you have the following 3 clusters, C1 through C3, with centroids m1 through m3. For any data point, we define its error as the distance between the data point and its cluster's centroid. SSE is then the sum of squared errors across all data points. A lower SSE means data points are generally close to their cluster centers, indicating high cohesion. 

However, SSE doesn't tell us about separation. The metric that captures both cohesion and separation is the Silhouette coefficient. Given a data point X in cluster C, we define two quantities. A(x) measures the average distance between X and other data points in the same cluster C -- a measure of cohesion, where a smaller A(x) indicates a tighter, more cohesive cluster. B(x) measures the smallest average distance between X and all data points in another cluster -- it captures how close X is to its nearest neighboring cluster; a larger B(x) means X is well separated from other clusters. The Silhouette coefficient of X is then calculated from A(x) and B(x). We can aggregate the Silhouette coefficients of all points in a cluster to reflect that cluster's quality, or average across all points to capture the quality of the entire clustering solution. A higher Silhouette coefficient implies B(x) is higher, A(x) is lower, or both -- meaning the clustering solution has both high cohesion and good separation.

**Visual**: use the same 3-cluster visualization as before, clearly mark the three clusters and their centroids. Then, respectively visualize the calculation of SSE and Silhouette coefficient in sync with the texts. For SSE, pick a random data point and highlight its distance to the centroid. Also show the SSE formula. Animate the formula's value shrinking as points move closer to their centroids, to illustrate "lower SSE = higher cohesion". For Silhouette coefficient, show the same data point with two elements: a set of short arrows to other points in the same cluster C labeled "A(x): avg. distance within cluster" and a set of arrows to the nearest neighboring cluster labeled "B(x): avg. distance to nearest cluster". Display the Silhouette coefficient formula combining A(x) and B(x).

# Scene 15

**Text**: With objective clustering quality metrics such as SSE, we can also pick the number of clusters by trying different numbers and plot the SSE measure against the number of clusters. Importantly, the best cluster solution is not the one that minimizes SSE -- when number of clusters equal number of data points, the SSE reduces to 0. Instead, we look for an "elbow" shape in the SSE plot -- a point where SSE drops sharply before, then becomes fairly flat after. Because SSE tends to drop as we increase the number of clusters, hitting an elbow point typically means we've found a natural number of clusters. 

**Visual**: show a line plot with number of clusters (K) on the x-axis and SSE on the y-axis, sharply decreasing then flattening out. Animate a callout circling the "elbow" at K=5, with a dashed vertical line dropping to the x-axis. 

# Scene 16

**Text**: Finally, suppose we have carried out clustering analysis and decided on a particular clustering solution, how do we interpret what each cluster means? Typically, we can interpret each cluster by its "average" data point, which is the centroid of the cluster -- formally, the mean of all data points in that cluster. It may or may not be an actual data point itself, but it nonetheless represents the average characteristics of the data in that cluster. 

More importantly, given the exploratory nature of clustering analysis, interpreting clustering results must be combined with domain knowledge. Think about whether the clusters make sense to you as a data scientist, and whether they help you solve the problem you set out to answer. Instead of trying to find the objectively best solution, keep in mind that there is no absolute "correct" clustering result -- your interpretation and evaluation depend on your business problem and goals.

**Visual**: show a cluster of scattered points with its centroid marked as a large C at the average position. Label the centroid "Cluster Profile". Then show a thought-bubble or checklist next to it: "Does this make sense given what I know about the business?" to emphasize the domain-knowledge step.
