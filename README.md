# WhatGenre
# A simple music genre classifier based on audio features and a dense neural network, with recommendations and a PyQt UI.


## It's necessary to fill the config.yaml file with a valid LastFm API key and user agent.

The model is trained on the GTZAN dataset, which offers a collection of 10 genres with 100 30-seconds samples each.
- Pop
- Reggae
- Metal
- Jazz
- Blues
- Disco
- Classical
- Hip hop
- Rock
- Country

## Packages used:
- Librosa
- Numpy
- Pandas
- TensorFlow
- PyQt 5 (for the UI)

The following features are extracted, using the Librosa package:
- Root Mean Square
- Chromagram
- Spectral Centroid
- Spectral Bandwidth
- Rolloff
- ZCR
- Harmonic Elements
- Percussive Elements
- Tempo
- MFCC

The model is a simple dense neural network of 4 fully-connected layers and one softmax output layer, trained for 500 epochs.

For inference, a random segment of at most 30 seconds is taken from the input audio file and its audio features are extracted and fed to the model.
After getting the predicted label, LastFM's API is used to get four random tracks from the first 2000 Top Tracks in the same genre. Clicking on a recommended song's name opens up a browser to a YouTube search of the said title. 

## Could be improved / added:
- the 30 seconds segment is too random and maybe not sufficient
- a more refined neural network architecture and training strategies
- a microphone recording feature (for which a button already exists but doesn't do anything)




