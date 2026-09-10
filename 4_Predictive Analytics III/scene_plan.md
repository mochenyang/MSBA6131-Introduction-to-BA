# Scene 1

**Text**: In this video, we're going to talk about two new tools for evaluating the performance of classifiers based on their class probability predictions: the ROC curve and AUC measure, and the cumulative response curve.

**Visual**: Title "Predictive Analytics" in center screen. Below it, subtitle "ROC Curve & AUC, Cumulative Response Curve" fades in.

# Scene 2

**Text**: As a quick reminder, many classification algorithms, including k-NN, decision tree, and naive Bayes, produce not only categorical predictions but also class probability predictions. A higher predicted probability means the classifier is more certain about its prediction, and categorical predictions are generated from these probabilities using a user-chosen cutoff. 

The choice of the cutoff value has some interesting implications, because classification results can look different under different cutoff values. Take this table as an example: 12 data points with their actual class labels and predicted probability of being in the positive class, ranked from high to low. Picking different cutoff values gives different classification results. If we pick the default cutoff of 0.5, all 12 records are predicted positive. If we instead pick a higher cutoff, say 0.8, only the top 7 records — the ones with probability higher than 0.8 — are predicted positive. The cutoff controls how aggressive or conservative the classifier behaves: a high cutoff means the classifier needs to be very certain before predicting positive, while a low cutoff lets it predict positive with relatively low confidence.

**Visual**: Title "Probability Cutoff and Classifier Performance" in center top. Below it, reuse the P(C_i | X) formula and the probability slider with cutoff elements from the "3_Predictive Analytics II" unit. These visuals will show up during the first paragraph of the text. Then they will fade out.

Next, a ranked table of 10 rows fades in and stays on the left half of the scene, with columns "Actual Class" (p/n) and "Predicted Probability," sorted high to low. Use the values below. Have another column called "Predicted Label" which is initially blank.
| Actual Class | Predicted Probability of $P$ |
| ------------ | ---------------------------- |
| $P$          | 0.99                         |
| $P$          | 0.98                         |
| $N$          | 0.96                         |
| $N$          | 0.90                         |
| $P$          | 0.88                         |
| $N$          | 0.87                         |
| $P$          | 0.85                         |
| $P$          | 0.80                         |
| $N$          | 0.70                         |
| $P$          | 0.65                         |

A horizontal cutoff line first appears below the bottom row, at 0.5, with all 10 rows labeled "Positive" under the "Predicted Class" column and marked green. The line then slides up to sit between rows 7 and 8; only the top 7 rows stay green as "Positive" while the rest turn yellow as "Negative" under the "Predicted Class" column. At each cutoff level, there should be a confusion matrix showing up on the right-hand-side of the table with the four cells filled up according to prediction results.

# Scene 3

**Text**: By picking different cutoff values, we can generate multiple sets of classification results for the same classifier, which reveals useful information about the classifier's quality. Let's use the same ranked list, but now think of it as the validation dataset. By gradually shifting the cutoff from high to low, we can generate a whole sequence of confusion matrices. The Receiver Operating Characteristic curve, or ROC curve in short, is an important tool to visualize model performance based on this sequence of confusion matrices. 

Specifically, the ROC curve plots the true positive rate against the false positive rate as the cutoff changes. The true positive rate is the same as the recall of class p, and the false positive rate is one minus the recall of class n. When cutoff value is the highest, all 10 records are predicted as negative. This amounts to 0% recall of positive and 1% recall of negative, corresponding to (0,0) on the ROC curve. As we move the cutoff down a notch, the first record is predicted as positive, producing 1/6 recall of positive while maintaining recall of negative at 1. This corresponds to (0, 1/6) on the ROC curve. This process continues until the cutoff moves below the smallest probability prediction, and all records are predicted as positive. 

**Visual**: Title "The ROC Curve" in center top. Below it, reuse the same 10-row ranked list from scene 2. Animate the cutoff line sweeping from above the top row down past the bottom row, one row at a time; at each stop, a small 2x2 confusion matrix appears beside the table and its counts update live. Simultaneously, to the right, empty ROC axes build up (x: False Positive Rate, y: True Positive Rate, both 0 to 1); each time the cutoff passes a row, plot a new dot at that confusion matrix's (FPR, TPR) coordinate and connect it to the previous dot, so the ROC curve visibly grows in sync with the cutoff sweep and the confusion matrix beside it.

# Scene 4

**Text**: Why is the ROC curve useful? Because it gives us a way to compare multiple classification models, both visually and quantitatively. Consider the ROC curves of four different classifiers, A through D. Curve A shoots straight up and then straight right — it corresponds to a perfect classifier, one that always assigns higher probabilities to every positive isntance than to every negative instancs. Curve D, close to the 45-degree diagonal line, corresponds to a random classifier that makes predictions based on a coin flip. A classifier that's better than random but not perfect will have an ROC curve that falls somewhere between A and D, and in general, the closer the curve sits to the top-left corner, the better the classifier.

In addition to visual comparison, the ROC curve also gives us a single-number measure of classifier performance: the area under the curve, or AUC. AUC is a number between 0 and 1 — 1 means a perfect classifier, 0.5 means a random classifier, and a reasonably good classifier should score somewhere between 0.5 and 1.

**Visual**: Title "ROC and AUC for Model Comparison" in center top. Below it on the left side of the scene, show a single ROC plot (axes FPR/TPR, 0 to 1) with four curves drawn: curve A hugging the top-left corner in a sharp right angle, labeled "A: perfect classifier"; curve D as the diagonal, labeled "D: random classifier"; two more curves B and C drawn in between at different distances from the top-left corner. As the narration describes each curve, highlight just that curve in a bright color while dimming the others. Finally, animate an arrow pointing to the top-left corner labeled "better," to reinforce that curves closer to this corner indicate better classifiers. On the right side of the scene, show "Area under the Curve (AUC)" as a smaller title, then show a single ROC curve and highlight its area under the curve, with texts below it showing "AUC = 1 -> perfect classifier"; "AUC = 0.5 -> random classifier"; "higher AUC -> better separation of the two classes".

# Scene 5

**Text**: At this point, it is worth pausing to ask the question of "WHY". Why can we look at the positions of the ROC curve to infer model performance, and why is the are under the ROC curve also associated with performance? Here's a useful way to think about ROC and AUC that will give you more intuition.

Remember how we built the ROC curve: sweeping down the ranked validation data points from highest predicted probability to lowest. Pay attention to the movements of the ROC curve, it moves up on every positive instance and moves right on every negative instance. This is expected, because moving cutoff below a positive instance would lead to one more true positive prediction, whereas moving cutoff below a negative instance would lead to one more false positive prediction.

This explains why an ROC curve positioned closer to the top-left corner indicates a better model. Intuitively, being closer to the top-left corner means the curve can go up for more steps before having to go right, which implies that it correctly ranks more positive instances ahead of negative instances based on probability predictions. If the ROC curve goes up all the way and then go right, it means that the model correctly ranks all positive instances ahead of negative ones, indicating a perfect classifier. 

Now, to understand what exactly AUC measures, imagine the space under the curve as a grid, with one column for every negative instance and one row for every positive instance. Every time the curve moves "up", it corresponds to a positive instance, and all the "right turns" to the right of this "up turn" correspond to the negative instances that have received lower probability predictions than the focal positive instance. So the shaded area under the curve is literally counting, across all positive-negative pairs, how often the positive instance scored higher than the negative one. Divide that count by the total number of pairs, and you get exactly the AUC. That's why AUC has such a clean interpretation: given one randomly chosen instance from class p and one from class n, call them X_1 and X_2, and let p(X_1) and p(X_2) denote the predicted probability of each instance belonging to the p class. Then AUC is the probability that p(X_1) is bigger than p(X_2) — in other words, it measures how well the model ranks truly positive instances ahead of truly negative ones.

**Visual**: Title "ROC and AUC: Intuitive Understanding" in center top. During the first two paragraphs of the narrative, reintroduce the same ranked list and animated ROC curve from scene 3. As the ROC curve grows, highlight the positive / negative class label just above the cutoff at each step.

During the third paragraph of narrative, bring back the four ROC curve visual from scene 4 and highlight curve A and B, respectively.

Then, during the last paragraph of narrative, overlay a faint grid on the ROC plot, with as many columns as there are negative points and as many rows as positive points in the running example, so the axes effectively read "number of negatives" by "number of positives." Replay the sweep row by row, and each time the curve makes an "up" move, shade in the grid cells to the right of the current column — building the region under the curve as a mosaic of unit squares rather than a smooth area. Meanwhile, highlight the p class instance that lead to the up move as well as all n class instances receiving lower predicted probabilities. Then use texts to define X_1 and X_2 as random instances from p class and n class respectively, and then build the formula "AUC = shaded cells / total cells = P(p(X_1) > p(X_2))" beneath the grid, with the shaded-cell count and total-cell count animating into the fraction. 

# Scene 6

**Text**: Let's turn to another model evaluation technique built on class probability predictions: the cumulative response curve. Like the ROC curve, the cumulative response curve is built from predicted class probabilities on a validation dataset. We first sort the data by predicted probability of being in the positive class, from high to low. Then, as we gradually move the cutoff threshold, more and more instances are predicted as the positive class. The x-axis of the curve is the percentage of validation data predicted as positive, and the y-axis is the cumulative response, which is the actual recall rate of the positive class at the given cutoff.

Just like the ROC curve, the cumulative response curve can also be used to compare multiple models. Every cumulative response curve starts at (0,0) and ends at (1,1), and the curve that sits closer to the top-left corner indicates a better classifier — it's able to "catch" more of the true positives within less of the data, meaning its probability predictions are more effectively ranking positive instances ahead of negative ones. The diagonal, 45-degree line represents the random classifier, where class predictions are made by flipping a coin.

**Visual**: Title "Cumulative Response Curve" at center top. Reuse the same ranked table of 10 validation records and the same visual style as the table from scene 2. Then build empty axes for the cumulative response curve (x: % of data, y: cumulative response). Use the exact same cutoff moving visual as the ROC part, show how the predicted values in the "Predicted Class" column change accordingly, and then plot the cumulative response curve in sync. 

During the second paragraph of narrative, showing several curves for different hypothetical models labeled A through D, plus the diagonal baseline labeled "random classifier." Highlight the curve closest to the top-left as "best" and the one closest to the diagonal as "weakest," with an arrow toward the top-left corner labeled "better" — following the same visual approach to "closer to this corner is better" callout used for the ROC curve in scene 4.

# Scene 7

**Text**: The cumulative response curve also lets us quantify exactly how much better a classifier is than random guessing. At any point on the x-axis, we divide the model's cumulative response by the random classifier's cumulative response at that same point; this ratio is called the lift ratio. For example, if a model's cumulative response at the top 20% of data is 1/3 while the random classifier's is 0.2, the lift ratio is 1/3 divided by 0.2, or about 1.7 — meaning the model's top 20% predictions are 1.7 times as good as random predictions.

We can plot this lift ratio at every point along the x-axis, which gives us the lift curve. A lift curve that sits higher and further to the right — closer to the top-right of the chart — indicates an overall better classifier.

**Visual**: Title "Lift Curve" at center top. Below it, split-screen. Left side: the cumulative response curve from scene 6, with a vertical dashed line at x=20%, showing the model's curve at height 1/3 and the diagonal random baseline at height 0.2 at that same x position; a bracket beside the two heights computes "(1/3) / 0.2 \approx 1.7." Right side: empty lift-ratio axes build up (x: % of data, y: lift ratio); as the dashed line sweeps left to right across the left chart, plot the corresponding lift-ratio value at each x position on the right chart, tracing out the lift curve in sync. Label the top-right area of the lift curve chart "better" once the full curve has been drawn.

# Scene 8

**Text**: To summarize, ROC curve and cumulative response curve are two representative examples of the so-called "ranking-based" evaluation methods. They both reflect how well a classification model ranks data instances based on predicted probabilities. It's useful to keep in mind that they differ from the evaluation metrics we discussed in a prior video, namely accuracy, precision, recall, and F-measure. To calculate these metrics, we need to first select a specific cutoff threshold to convert probability predictions into class predictions. In comparison, ROC curve (and by extension the AUC measure) as well as the cumulative response curve are "threshold-agnostic" because their construction requires the enumeration of all possible cutoff values. Changing the cutoff threshold in a classification model does not change its ROC curve or cumulative response curve.

**Visual**: Title "Summary: Ranking-based Evaluation Methods" at center top. Below it, split screen and within the left half, show ROC curve from scene 3 and cumulative response curve from scene 6 in smaller boxes side-by-side, under title "Ranking-based Methods". In the right half, show a confusion matrix and "Accuracy", "Precision", "Recall, "F-measure" below it. Follow the narrative, fade in "Do not change w.r.t. cutoff" in left-half and "Depend on specific cutoff" in right-half.