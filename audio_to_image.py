import numpy as np
import librosa
import matplotlib.pyplot as plt
import matplotlib
import soundfile as sf


# y is the amplitude, sr is the sample rate
# liborsa load takes in a .wav file format (.mp3 does not work)
y, sr = librosa.load("test.wav")

print(sr)
# zoom = 50
# y = y[0:zoom]

# librosa.display.waveshow(y)
crossings = librosa.feature.zero_crossing_rate(y)
print(len(crossings[0]))

# print(len(y))
# print(len(crossings))

# # print(crossings)

# t = np.linspace(0, 5, num=len(y))
# plt.scatter(t, crossings, color='r', linewidths=0.7)
# plt.show()

# plt.figure(figsize=(30,30))
# plot_audio = librosa.load("./sample.wav")
# zoom = 50

# print(plot_audio)