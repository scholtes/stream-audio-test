# Python 3.5 or greater
#     $ pip install pyaudio
#     $ python shepard-tones-gui.py
# 
# See shepard-tones.py for description.
# Basicallly the same thing, except there's a GUI around it
import importlib
shepardtones = importlib.import_module("shepard-tones")

import pyaudio
import itertools
import struct
import asyncio
import threading
import tkinter as tk

#=====================
# CHeck chrome bookmarks folder "scripts" for stack overflow things
# TODO: remove this comment
# (if you see this it's because I was going to embed the Desmos graph)
#====================

class App():
    CENTER = shepardtones.CENTER
    VOL = shepardtones.VOL
    K = shepardtones.K
    N = shepardtones.N
    OPS = shepardtones.OPS

    def __init__(self):
        pass

    def main(self):
        p = pyaudio.PyAudio()
        g = shepardtones.dualchunk()
        next(g)
        stream = p.open(format=pyaudio.paFloat32,
            channels=shepardtones.CHANNELS,
            rate=shepardtones.Fs,
            output=True)
        while True:
            stream.write(g.send([
                self.K,
                self.N,
                self.VOL,
                self.OPS,
                self.CENTER
            ]))

    def asyncmain(self):
        thread = threading.Thread(target = self.main)
        thread.daemon = True
        thread.start()
        return thread

    def do_gui(self):

        def updateCENTER(e):
            self.CENTER = w_CENTER.get()
        def updateVOL(e):
            self.VOL = w_VOL.get()
        def updateK(e):
            self.K = w_K.get()
        def updateN(e):
            self.N = w_N.get()
        def updateOPS(e):
            self.OPS = w_OPS.get()

        master = tk.Tk()
        master.title('Shepard Tone generator')

        tk.Label(master, text="Center Frequency (Hz)").pack()
        w_CENTER = tk.Scale(master, from_=20, to=880, length=600, orient='horizontal', command=updateCENTER)
        w_CENTER.set(self.CENTER)
        w_CENTER.pack()

        tk.Label(master, text="Volume").pack()
        w_VOL = tk.Scale(master, from_=0, to=1, length=600, resolution=0.001, orient='horizontal', command=updateVOL)
        w_VOL.set(self.VOL)
        w_VOL.pack()

        tk.Label(master, text="Frequency balance").pack()
        w_K = tk.Scale(master, from_=0.1, to=10, length=600, resolution=0.001, orient='horizontal', command=updateK)
        w_K.set(self.K)
        w_K.pack()

        tk.Label(master, text="Number of octaves / 2").pack()
        w_N = tk.Scale(master, from_=1, to=shepardtones.MAX_N, length=600, orient='horizontal', command=updateN)
        w_N.set(self.N)
        w_N.pack()

        tk.Label(master, text="Octaves per second").pack()
        w_OPS = tk.Scale(master, from_=-3, to=3, length=600, resolution=0.001, orient='horizontal', command=updateOPS)
        w_OPS.set(self.OPS)
        w_OPS.pack()

        tk.mainloop()

if __name__ == '__main__':
    app = App()
    app.asyncmain()
    app.do_gui()