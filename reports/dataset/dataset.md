# Dataset Description

An essential aspect in addressing this problem lies in obtaining an appropriate dataset. Let's revisit the problem statement: our objective is to eliminate audience clapping from classical music performances. Consequently, this translates into a classification challenge, where our task is to identify whether a segment of sound (audio) corresponds to audience clapping or not. We can then recommend its removal based on this classification (or prediction).

To achieve this, we'll classify sound segments into two distinct classes: 'yes' and 'no.' The 'yes' class denotes audio segments with audience clapping, while the 'no' class encompasses segments without clapping, including silence before or after the performance and the classical music itself.

Acquiring the dataset involves downloading classical music audio primarily from platforms like YouTube. To pinpoint audience clapping, we need to define the duration of each audio segment. I conducted an exploration of various durations, detailed in the 'duration-exploration.ipynb' notebook. It appears that a duration of approximately 1.8 seconds captures the typical audible length of audience clapping.
