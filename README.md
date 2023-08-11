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
1. There is a sample audio named "sample.mp3". Have a listen to the audio and you will notice that there are two parts where the audiences clap, at the start and at the end.
2. The models are already trained. Hence, the only step you need to do is "make remove_claps". This will run the "remove_claps.py" in the src folder. It will output an audio name "result0.mp3"
3. The result is not as clean but it achieves what I have in mind.

