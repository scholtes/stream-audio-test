import pyaudio
import math
import itertools
import struct
import asyncio
import threading

CHUNK = 1024
CHANNELS = 2
VOL = 0.25
Fs = 44100
F1 = 440
F2 = 550

def wavegen():
    theta = 0.0
    yield None
    while True:
        f = yield VOL*math.sin(theta)
        theta += 2.0*math.pi*f/Fs

def dualchunk():
    g1 = wavegen()
    g2 = wavegen()
    next(g1)
    next(g2)
    f1 = 0
    f2 = 0
    yield None
    while True:
        slice1 = [0]*(CHUNK//2)
        slice2 = [0]*(CHUNK//2)
        for i in range(CHUNK//2):
            slice1[i] = g1.send(f1)
            slice2[i] = g2.send(f2)
        interlace = [j for i in zip(slice1, slice2) for j in i]
        bits = struct.pack('{}f'.format(CHUNK), *interlace)
        f = yield bits
        f1 = f[0]
        f2 = f[1]

def main():
    p = pyaudio.PyAudio()
    g = dualchunk()
    next(g)
    stream = p.open(format = pyaudio.paFloat32, channels = 2, rate = Fs, output = True)
    while True:
        stream.write(g.send([F1, F2]))

def asyncmain():
    thread = threading.Thread(target = main)
    thread.daemon = True
    thread.start()
    return thread


if __name__ == '__main__':
    main()