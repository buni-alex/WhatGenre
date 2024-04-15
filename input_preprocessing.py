import librosa
import numpy as np

def extract_info(song, sr, fit):
    rms = librosa.feature.rms(y = song, frame_length=1024, hop_length=512)
    chroma_stft = librosa.feature.chroma_stft(y=song, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=song, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=song, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=song, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y = song)
    harmony = librosa.effects.harmonic(y = song)
    tempo = librosa.beat.tempo(y = song, sr = sr, hop_length=512)[0]
    perceptr = librosa.effects.percussive(y = song)
    mfcc = librosa.feature.mfcc(y=song, sr=sr)

    info = [[np.mean(chroma_stft)], [np.var(chroma_stft)], [np.mean(rms)], [np.var(rms)], [np.mean(spec_cent)], [np.var(spec_cent)], [np.mean(spec_bw)], [np.var(spec_bw)], [np.mean(rolloff)], [np.var(rolloff)], [np.mean(zcr)], [np.var(zcr)], [np.mean(harmony)], [np.var(harmony)], [np.mean(perceptr)], [np.var(perceptr)], [tempo]]
    for e in mfcc:
        info.append([np.mean(e)])
        info.append([np.var(e)])
    info = np.array(info, dtype = np.float64)
    info = np.reshape(info, [-1, 57])

    info = fit.transform(info)

    return info