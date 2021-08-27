# Python 3.5 or greater
#     $ pip install pyaudio
#     $ python shepard-tones.py
# 
# This example plays shepard tones
# 
# Values:
#   center - [0 to 20000] The central frequency (in Hertz)
#   vol - [0 to 1] the amplitude ("volume")
#   k - [0 to infinity] larger values make the "central" frequency more pronounced
#   n - [1 to infinity] the number of octaves above and below the center frequency
#           - values above 5 might struggle to run in real time
#   ops - rate of change of the tone (octaves per second). Negative numbers descend
#   
# 
# Some examples to try:
#   
#    # Use the defaults
#   python shepard-tones.py
# 
#   # Equivalent to the defaults
#   python shepard-tones.py --center 110 --vol 0.9 --k 8 --n 4 --ops -0.1
#
#   # Rising shepard tone (1 octave in 5 seconds), centered around A4 (440Hz)
#   python shepard-tones.py --center 440 --ops 0.2
#
#   # Same as above but with different frequency balance
#   python shepard-tones.py --center 440 --k 1.4 --ops 0.2
#   
#   # Same as above but there are fewer frequencies present
#   python shepard-tones.py --center 440 --k 1.4 --n 2 --ops 0.2 
# 
#  # 220 Hz, k=5 frequency balance, 8 octaves (n*2), 0.08 octaves per second
#  python shepard-tones.py --center 220 --k 5 --n 4 --ops 0.08
#
# See https://www.desmos.com/calculator/suceawvzsl
# Play with the sliders!
# 
# If the audio is chirping, it's because your machine is struggling to run this in real time.
# Try closing some applications (like Chrome and the Desmos tab).

import pyaudio
import argparse
import math
import struct

CHUNK = 1024 # 1024 works but is a bit iffy... make more efficient and/or.... ???
CHANNELS = 2 # Number of channels (stereo = 2, mono = 1)
Fs = 44100 # Sampling frequency (try 8000 if experience slowness)

CENTER = 110 # Central frequency
VOL = 0.9 # Amplitude
K = 8 # The higher this value, the more pronounced the dominant frequency is
N = 4 # Half of the number of octaves present
OPS = -0.1# Octaves per second increase (negative goes down)

def bump(x):
    if -1<x and x<1:
        return math.exp(1-1/(1-x**2))
    else:
        return 0

def amp(x,k,n):
    return bump(x/n)**k

MAX_N = 7
def wavegen():
    theta = 0.0
    k = K
    n = MAX_N
    vol = VOL
    ops = OPS
    center = CENTER
    offset = 0 # Desmos "f" (number of octaves offset over time)

    theta = [0.0]*(2*n)
    amps = [1.0]*(2*n) # y-coord of Desmos "(F,A(F))"
    freqs = [1.0]*(2*n) # Desmos "center * 2**(F)"
    base_octaves = list(range(-n,n)) # Desmos "B"
    adj_octaves = list(range(-n,n)) # Desmos "F"

    yield None
    while True:
        offset += ops / Fs
        #offset = offset % 1.0 # Also doesn't work???
        for i in range(2*n):
            adj_octaves[i] = ((base_octaves[i] + offset + n) % (2*n)) - n
            freqs[i] = center * (2**adj_octaves[i])
            amps[i] = amp(adj_octaves[i], k, n)
        norm = sum(amps)
        k,n,vol,ops,center = yield sum(vol*amps[i]*math.sin(theta[i]) for i in range(2*n))/norm
        for i in range(2*n):
            theta[i] += 2.0*math.pi*freqs[i]/Fs
            #theta[i] = theta[i] % (Fs/freqs[i]) # Doesn't work for some reason????

def dualchunk():
    k = K
    n = N
    vol = VOL
    ops = OPS
    center = CENTER

    g1 = wavegen()
    next(g1)
    yield None
    while True:
        slice1 = [0]*(CHUNK//2)
        for i in range(CHUNK//2):
            slice1[i] = g1.send([k,n,vol,ops,center])
        interlace = [j for i in zip(slice1, slice1) for j in i]
        bits = struct.pack('{}f'.format(CHUNK), *interlace)
        k,n,vol,ops,center = yield bits

def main():
    parser = argparse.ArgumentParser(description="Generate shepard tones in real time")
    parser.add_argument("-c", "--center", type=float, default=CENTER, help="")
    parser.add_argument("-v", "--vol", type=float, default=VOL, help="")
    parser.add_argument("-k", "--k", type=float, default=K, help="")
    parser.add_argument("-n", "--n", type=int, default=N, help="")
    parser.add_argument("-o", "--ops", type=float, default=OPS, help="")
    args = parser.parse_args()

    p = pyaudio.PyAudio()
    g = dualchunk()
    next(g)
    stream = p.open(format=pyaudio.paFloat32, channels=CHANNELS, rate=Fs, output=True)
    while True:
        stream.write(g.send([
            args.k,
            args.n,
            args.vol,
            args.ops,
            args.center
        ]))


if __name__ == "__main__":
    main()
