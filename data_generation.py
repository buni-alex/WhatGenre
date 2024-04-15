#%%
import os
import pathlib
import csv
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import librosa

#%%

cmap = plt.get_cmap('inferno')
plt.figure(figsize=(10,10))

#%%
genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
#%%
for g in genres:
  path_audio = os.path.join('./3secs',f'{g}')
  os.makedirs(path_audio)

#%%
for g in genres:
  j=-1
  print(f"{g}")
  for filename in os.listdir(os.path.join('./GTZAN Dataset/Data/genres_original',f"{g}")):
    song = os.path.join(f'./GTZAN Dataset/Data/genres_original/{g}',f'{filename}')
    j = j+1
    for w in range(0,10):
      t1 = 3*(w)*1000
      t2 = 3*(w+1)*1000
      newAudio = AudioSegment.from_wav(song)
      new = newAudio[t1:t2]
      new.export(f'./3secs/{g}/{g+str(j)+str(w)}.wav', format="wav")


#%%
for g in genres:
    pathlib.Path(f'img_data/{g}').mkdir(parents=True, exist_ok=True)     
    for filename in os.listdir(f'./3secs/{g}'):
        songname = f'./3secs/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=5)
        plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB')
        plt.axis('off')
        plt.savefig(f'img_data/{g}/{filename[:-3].replace(".", "")}.png')
        plt.clf()
 
#%% 
header = 'filename chroma_stft_mean crhoma_stft_var rms_mean rms_var spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean spectral_bandwidth_var rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean harmony_var perceptr_mean perceptr_var tempo'
for i in range(1, 21):
    header += f' mfcc{i}_mean'
    header += f' mfcc{i}_var'
header += ' label'
header = header.split()

#%%
file = open('data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)
genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
for g in genres:
    for filename in sorted(os.listdir(f'./3secs/{g}'), key = len):
        songname = f'./3secs/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=3)
        rms = librosa.feature.rms(y = y, frame_length=1024, hop_length=512)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        harmony = librosa.effects.harmonic(y = y)
        tempo = librosa.beat.tempo(y = y, sr = sr, hop_length=512)[0]
        print(songname)
        perceptr = librosa.effects.percussive(y = y)
        to_append = f'{filename} {np.mean(chroma_stft)} {np.var(chroma_stft)} {np.mean(rms)} {np.var(rms)} {np.mean(spec_cent)} {np.var(spec_cent)} {np.mean(spec_bw)} {np.var(spec_bw)} {np.mean(rolloff)} {np.var(rolloff)} {np.mean(zcr)} {np.var(zcr)} {np.mean(harmony)} {np.var(harmony)} {np.mean(perceptr)} {np.var(perceptr)} {tempo}'    
        for e in mfcc:
            to_append += f' {np.mean(e)}'
            to_append += f' {np.var(e)}'
        to_append += f' {g}'
        file = open('data.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())

# %%
