# Python 3.5 or greater
#     $ pip install pyaudio
#     $ python shepard-tones.py
import pyaudio
import math
import struct

#+=====================
# CHeck chrome bookmarks folder "scripts" for stack overflow things
# TODO: remove this comment
#====================

CHUNK = 1024 # 1024 works but is a bit iffy... make more efficient and/or.... ???
CHANNELS = 2
Fs = 44100

CENTER = 110 # Central frequency
VOL = 0.8 # Amplitude
K = 10 # The higher this value, the more pronounced the dominant frequency is
N = 5 # Half of the number of octaves present
OPS = -0.1# Octaves per second increase (negative goes down)

def bump(x):
    if -1<x and x<1:
        return math.exp(1-1/(1-x**2))
    else:
        return 0

def amp(x,k,n):
    return bump(x/n)**k

def wavegen():
    theta = 0.0
    k = K
    n = N
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
    p = pyaudio.PyAudio()
    g = dualchunk()
    next(g)
    stream = p.open(format = pyaudio.paFloat32, channels = 2, rate = Fs, output = True)
    while True:
        stream.write(g.send([K,N,VOL,OPS,CENTER])) # TODO: send this variably (see play.py)

class App():
    pass


if __name__ == "__main__":
    main()
