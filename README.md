# stream-audio-test
Experiment with lazy real time audio streaming in python.

Problem: we want to play audio that reacts to parameters that vary in real time, and keep multiple audio channels in sync in real time.  This small program serves as code example on how to go about achieving this in python.

In this demo, we control the frequency of pure sinusoidal tones to two stereo channels with an interactive GUI. 

## Setup
python 3.5 or later 

```
$ pip install pyaudio
```

## Use
```
$ python play.py
```