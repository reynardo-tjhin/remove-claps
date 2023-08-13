# Remove Audience Clapping from a Classical Music Audio

## Tutorials (on Audio Analysis):
I learned Audio Analysis from a Youtube Series:
![Audio Signal Processing for Machine Learning](https://www.youtube.com/playlist?list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0)
<br>
Thanks to ![Valerio Velardo](https://www.youtube.com/@ValerioVelardoTheSoundofAI)

## Description:
The challenge at hand is to create a specialized tool that enhances the offline listening experience of classical music performances, particularly when sourced as MP3 files. Classical music recordings often include audience clapping. These section detracts from the immersive and focused listening experience that many classical music enthusiasts seek. To address this issue, this project aims to develop a solution that allows users to seamlessly eliminate or skip these audience clappings, ensuring that the essence of the performance is preserved while enhancing user enjoyment. This project involves downloading datasets, extracting audio features, training algorithms, and ultimately creating a tool capable of enhancing MP3 audio by removing audience clapping, resulting in a more refined listening experience.

**Note**: The availability of YouTube video links is uncertain. Therefore, the 'data-features' folder is designed to retain the essential features of downloaded MP3 audio, ensuring data preservation.

## Dataset:
The dataset is sourced by downloading video audio from YouTube (from 'music_links.csv') and subsequently converting it to the WAV format. The 'yes' and 'no' classes are determined by detecting instances of audience clapping, then recorded in 'new_dataset.csv'. Following this, the features are extracted and stored within the 'data-features' folder.

## How to try:
1. Download the audios from YouTube by executing './download.sh [YOUTUBE_LINK] [DESIRED_FILE_NAME]'. This command runs 'download.py' from the 'src' folder.
2. The models are pre-trained, simplifying the process to a single step: execute './remove_claps.sh [FILENAME]'. This command runs 'remove_claps.py' from the 'src' folder, generating an audio file named 'result[no].mp3' as the output.
3. The output may not be perfect in terms of cleanliness, but it successfully aligns with the intended goal.

Some youtube links to try:
- [Yuja Wang - Turkish March Mozart (Encore)](https://www.youtube.com/watch?v=pHM52-QR-e0)
- [Piano Recital - Mozart, Chopin, Schumann and Rachmaninoff - Anna Fedorova](https://www.youtube.com/watch?v=V5cerHBgMDw)
- [Mozart: Violin Concerto No.3 - Hilary Hahn /Gustavo Dudamel /Stuttgart Radio Symphony Orchestra](https://www.youtube.com/watch?v=IhQAtkXOK6o)
