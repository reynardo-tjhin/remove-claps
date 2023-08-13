# Report

A concise report aimed at summarizing the various project steps and sections.

## Datasets

An essential aspect in addressing this problem lies in obtaining an appropriate dataset. Let's revisit the problem statement: our objective is to eliminate audience clapping from classical music performances. Consequently, this translates into a classification challenge, where our task is to identify whether a segment of sound (audio) corresponds to audience clapping or not. We can then recommend its removal based on this classification (or prediction).

To achieve this, we'll classify sound segments into two distinct classes: 'yes' and 'no.' The 'yes' class denotes audio segments with audience clapping, while the 'no' class encompasses segments without clapping, including silence before or after the performance and the classical music itself.

Acquiring the dataset involves downloading classical music audio primarily from platforms like YouTube. To pinpoint audience clapping, we need to define the duration of each audio segment. I conducted an exploration of various durations, detailed in the 'duration-exploration.ipynb' notebook. It appears that a duration of approximately 1.8 seconds captures the typical audible length of audience clapping.

To maintain dataset balance, a random selection of audio instances is removed, ensuring an equal representation of 'yes' and 'no' class instances. This step is crucial to prevent the training process from biasing the model towards one class during testing.

## Obtaining Audio Features from the Downloaded Audio?

Audio signals can be characterized by various audio features, including root-mean-square, zero-crossing rate, spectral bandwidth, etc. The audio segments, each lasting 1.8 seconds, undergo calculation of these audio features. The following features are utilized:

- Root-Mean-Square Energy
- Zero-Crossing Rate
- Spectral Centroid
- Spectral Bandwidth
- Spectral Flatness
- Spectral Rolloff

The mean and standard deviation of these features are then computed.

## Training using Multiple Models

Once we've obtained the tabulated audio features, we employ Machine Learning techniques to classify whether a 1.8-second audio segment belongs to the 'yes' class or the 'no' class. The following models are utilized for this purpose:

- Support Vector Classifier
- Extra Trees Classifier
- Linear Discriminant Analysis
- Decision Trees Classifier
- K-Nearest Neighbors Classifier
- Random Forest Classifier
- Multilayer Perceptrons Classifier
- AdaBoost Classifier
- Nu-Support Classifier
- Gaussian Naive Bayes Classifier

## Training Results

Remarkably, the models achieve excellent results (over 94%) with minimal hyperparameter adjustments, possibly due to the distinct separation between 'yes' and 'no' class instances. This raises the question whether machine learning models are truly necessary for this audio classification. Additionally, some classifiers exhibit signs of overfitting, with training metrics such as accuracy, F1 score, precision, and recall reaching 100%. Considering accuracy on the testing set as the primary metric, the multi-layer perceptron classifier appears to be the most suitable choice.

## Next Work

The current project tackles the issue through iterative audio segment classification. Future efforts may concentrate on refining this existing approach to enhance problem-solving methods.

## Some Notable Works/Information that have helped me

- [ESC-50: Environmental Sound Classification](https://www.kaggle.com/code/salimhammadi07/esc-50-environmental-sound-classification/notebook)
- [Audio Signal Processing for Machine Learning](https://www.youtube.com/playlist?list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0)

