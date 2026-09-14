# Scene 1

**Text**: In this video, we'll cover two important topics in predictive analytics: cross validation, a robust way to evaluate the performance of a predictive model, and feature selection, a set of techniques for choosing which features to include in a predictive model.

**Visual**: Title "Predictive Analytics" in center screen. Below it, subtitle "Cross Validation & Feature Selection" fades in.

# Scene 2

**Text**: In a previous video, we talked about using the training-validation split to evaluate the performance of a predictive model: we split the labeled data randomly into a training set and a validation set, build the model on the training set, and evaluate it on the validation set to get a performance measure that's less affected by overfitting.

Cross validation is a generalization of the same idea. It relies on a user-chosen parameter, k, that determines the number of random subsets to create — one subset is often called a "fold". During a k-fold cross validation, we randomly partition the labeled dataset into k equal-sized subsets. In each round, we use k-1 folds to build the predictive model, and evaluate its performance on the remaining fold. This process is then repeated for k rounds.

For example, in a 5-fold cross validation, the labeled data is first partitioned into 5 subsets. In each round, 4 folds are used to build a decision tree, and the remaining fold is used to evaluate the performance of that tree.

**Visual**: Title "Cross Validation: Intuition and Procedure" in center screen. First show the same training-validation from scene 5 in unit 2 (/home/mochen/MSBA6131-Introduction-to-BA/2_Predictive Analytics I/scenes/scene_05.py) but remove the unlabeled data part (just show training validation split). Then, this fades out and the main visual appears. On left-side of the screen, show peudocode for general k-fold cross validation. On right-side of the screen, show a horizontal bar of dots representing the labeled dataset splits into 5 equal-colored segments labeled Fold 1 through Fold 5. Below it, animate 5 rounds one at a time, left to right: in each round, 4 folds highlight green and label "Training," the remaining fold highlights orange and labels "Validation"; a small gear icon (symbolizing the model) appears above the training folds each round, with an arrow from it to the validation fold producing a performance score (labeled score_1 to score_5 in latex). After round 5, show all 5 performance scores lined up beneath the bar.

# Scene 3

**Text**: So how do we obtain performance results from cross validation? There are two ways to do it. First, we can aggregate the performance measures across rounds: in each of the k rounds we obtain a performance score (such as accuracy) — we can then report the mean and standard deviation of those k performance scores. Second, we can combine the predictions from each round's validation fold into one pooled set of predictions, and then calculate the performance measure directly on that combined set. Either approach is valid for reporting cross-validation performance, though they may not necessarily give the same results.

**Visual**: Title "Cross Validation: Reporting Evaluation Results" in center screen. Split-screen, both sides reusing the same 5-fold setup from scene 2. Left, titled "Aggregate Per-Round Measures": 5 performance scores (score_1 through score_5 in latex) appear one per round, then combine into mean and standard deviation formulas. Right, titled "Pool Predictions First": the 5 validation folds' predictions merge into a single combined table, and one performance score is computed from that pooled table. 

# Scene 4

**Text**: To summarize, compared to to a single training-validation split, is that cross validation tends to produce a more robust and stable estimate of a model's performance. In a single split, we might happen to get a validation dataset that's too easy or too hard to predict, simply due to random chance — and as a result, the model's performance can be under- or overestimated because of an unlucky split.

Cross validation is much more robust against this problem, because every data point ends up in the validation fold at exactly one round, and aggregating performance across all rounds gives a more stable measure. As a bonus, if we observe that performance varies dramatically across rounds, that's actually a useful signal — it suggests the labeled data may be too noisy or too small.

**Visual**: Title "Cross Validation: Summary" in center screen. Below it, show two first-level checkboxes: 1. "Single training-validation split can produce unstable results"; under it, two sub-bullets: "Validation set too easy -> overestimate performance" and "Validation set too hard -> underestimate performance." 2. "Cross validation provides more robust performance evaluation" with three sub-bullets: "Every data point is in validation fold once," "Aggregating performance across rounds gives stable measure," and "High variance across rounds signals noisy or small dataset."

# Scene 5

**Text**: Another important topic in predictive analytics is feature selection. The goal of feature selection is to select only the best, most predictive features to use in building a predictive model. The first question worth asking is, why bother? Isn't more information always better?

Actually, more features isn't always better. Having irrelevant or low-quality features can hurt a predictive model's performance. Consider the k-nearest neighbor model as an example: if some features aren't useful for prediction, including them in the data can distort the distance calculations and cause the model to perform poorly.

We've actually already seen one feature selection approach in action: the recursive partitioning algorithm behind decision trees automatically selects the best feature to split on at each step, based on the information gain metric.

**Visual**: Title "Feature Selection" in center screen and "Selecting the best features for predictive modeling" as subtitle. Below it, reuse the k-nn and decision tree visuals from /home/mochen/MSBA6131-Introduction-to-BA/3_Predictive Analytics II/scenes/scene_02.py, but no need to show the prediction probability calculations or animations. Instead, for k-NN, show text under it saying "distance are sensitive w.r.t. irrelevant features." For decision tree, show text under it saying "choosing splits based on information gain is a form of feature selection."

# Scene 6

**Text**: More generally, feature selection approaches fall into two types: the filter approach and the wrapper approach. We will focus on the filter approach first. The idea is to filter out uninformative features before the model is built, and doing so requires having a good definition of feature informativeness, or feature importance. A number of importance measures are available: information gain, which is used by the decision tree algorithm; correlation between a feature and the outcome, where higher correlation indicates a more predictive feature; and the chi-squared statistic, which indicates a feature's ability to separate different outcome classes. After choosing an importance measure, we rank all features and pick the top K to build the predictive model.

**Visual**: Title "General-Purpose Feature Selection: Filter Approach and Wrapper Approach", and then the "and Wrapper Approach" text fades out then subtitle "Select by feature importance measure before building the model" fades in. Below it, show a funnel figure with a list of feature names (X_1, X_2, etc. in latex) entering from the left. Then some features exit the funnel to the right, while others don't make it out. When a feature makes it through, show a green checkmark on top of the funnel, and when a feature doesn't make it through, show a red X on top of the funnel. Below the funnel, three importance-measure bullets appear one at a time: "Information Gain / Gain Ratio," "Correlation with Outcome," "Chi-Squared Statistic."

# Scene 7

**Text**: Compared to the filter approach, the wrapper approach relies on the performance of actual models to determine which features to use. There are two standard wrapper approaches: forward selection and backward elimination. The idea behind them is the same, except they work in opposite directions. 

Forward selection starts with a single feature and adds one more feature at a time until performance stops improving. More specifically, say the set of all features is X_1 through X_5. Under forward selection, we start by using each single feature on its own to build a model, and select whichever feature produces the best-performing model. Next, we use that selected feature together with each of the other remaining features, one at a time, to build a model, and keep whichever combination performs best. We repeat this process, adding one feature at a time, until performance no longer improves.

Backward elimination starts with all the features and drops one feature at a time until performance stops improving. We start with all the features, then try dropping each feature one at a time and rebuilding the model, eliminating whichever feature's removal results in the best performance improvement. We again repeat this process, dropping one feature at a time, until performance no longer improves.

**Visual**: Title "General-Purpose Feature Selection: Wrapper Approach" and subtitle "Select features based on actual model performance." Below it, split screen and show title "Forward Selection" on the left and "Backward Elimination" on the right.

Under "Forward Selection", Show a horizontal row of feature boxes labeled X_1 through X_5. Under that, gradually show Round 1, Round 2, etc. In Round 1, each single feature will light up one at a time, and X_3 will be highlighted by a box as the best feature and written as "Round 1: X_3 selected". Next, in Round 2, X3 will keep its highlight box and each of the other features will light up one at a time, and X_1 will be highlighted by a box as the best feature and written as "Round 2: {X_3, X_1} selected". Then Round 3: just say "repeat until performance does not improve."

Under "Backward Elimination", Reuse the same feature set X_1 through X_5 and the round-based structure. This time, Round 1 will show all features highlighted together, labeled "Round 1: Full Model". Then, Round 2 will show each feature being un-highlighted one at a time, and the X_2 is crossed-out with text saying "Round 2: X_2 dropped". Then Round 3 simply says ""repeat until performance does not improve."
