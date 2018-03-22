# Python 3.5 or greater
#     $ pip install pyaudio
#     $ python play.py
import pyaudio
import math
import itertools
import struct
import asyncio
import threading
import tkinter as tk

class App():
    CHUNK = 1024
    CHANNELS = 2
    VOL = 0.25
    Fs = 44100
    F1 = 440
    F2 = 550

    def __init__(self):
        pass

    def wavegen(self):
        theta = 0.0
        yield None
        while True:
            f = yield self.VOL*math.sin(theta)
            theta += 2.0*math.pi*f/self.Fs

    def dualchunk(self):
        g1 = self.wavegen()
        g2 = self.wavegen()
        next(g1)
        next(g2)
        f1 = 0
        f2 = 0
        yield None
        while True:
            slice1 = [0]*(self.CHUNK//2)
            slice2 = [0]*(self.CHUNK//2)
            for i in range(self.CHUNK//2):
                slice1[i] = g1.send(f1)
                slice2[i] = g2.send(f2)
            interlace = [j for i in zip(slice1, slice2) for j in i]
            bits = struct.pack('{}f'.format(self.CHUNK), *interlace)
            f = yield bits
            f1 = f[0]
            f2 = f[1]

    def main(self):
        p = pyaudio.PyAudio()
        g = self.dualchunk()
        next(g)
        stream = p.open(format = pyaudio.paFloat32, channels = 2, rate = self.Fs, output = True)
        while True:
            stream.write(g.send([self.F1, self.F2]))

    def asyncmain(self):
        thread = threading.Thread(target = self.main)
        thread.daemon = True
        thread.start()
        return thread

    def do_gui(self):

        def updateF1(e):
            self.F1 = w1.get()
        def updateF2(e):
            self.F2 = w2.get()

        master = tk.Tk()

        w1 = tk.Scale(master, from_=400, to=800, length=1000, orient='horizontal', command=updateF1)
        w1.set(self.F1)
        w1.pack()

        w2 = tk.Scale(master, from_=400, to=800, length=1000, orient='horizontal', command=updateF2)
        w2.set(self.F2)
        w2.pack()

        tk.mainloop()


if __name__ == '__main__':
    app = App()
    app.asyncmain()
    app.do_gui()