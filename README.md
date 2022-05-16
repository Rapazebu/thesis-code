This repository contains codes and data for the clustering I performed on my MA thesis project.

The folder **Task1 - SVM** contains scripts and codes of the classifier for word sense disambiguation.
The folder **Task2 - kmeans clustering** contains scripts and codes of the clustering for verb classes induction.

The Task2 folder is further divided into three subfolders:

**2.1. Clustering static embeddings** shows the clustering of the Sketch Engine Embeddings made on ItWac (https://embeddings.sketchengine.eu/static/index.html). I used all the verbs from the lowercased lemmatized ones.

**2.2. Clustering mean contextual BERT embeddings** shows the clustering of the means of the contextualixed BERT embeddings derived from verbs in sentences for each pattern.

**2.3. Clustering database features** shows the clustering of the database features (selectional preferences + subcategorization frames) as encoded in the database. the letters G, M and R are three different algorythms I used for encoding the features, two (M and R) trying to preserve the hierarchy between semantic types and one (G) not.

K-means was run using scipy for word2vec (see the script "k-means-clustering.py") and sklearn for categorical features (scipy kmeans do not allow sparse matrixes).

The k parameter, i. e. the number of clusters, is varied for each task at k = 15, k = 30, k = 40. Results are stored in the .txt files.
