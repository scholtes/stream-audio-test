# Python 3.5 or greater
#     $ pip install pyaudio
#     $ python playthrough.py
# 
# This example passes microphone input directly to the speaker.
# Use headphones to avoid feedback loop.
#

import pyaudio
import math
import itertools
import struct
import asyncio
import threading
import tkinter as tk

CHUNK = 1<<9
FORMAT = pyaudio.paFloat32 # pyaudio.paInt16
RATE = 44100
MAX_CHANNELS = 2


def passthrough(**kwargs):
    device_in = kwargs.get('device_in')
    device_out = kwargs.get('device_out')

    p = pyaudio.PyAudio()
    channels_in = p.get_device_info_by_host_api_device_index(0, device_in) if device_in else MAX_CHANNELS
    channels_out = p.get_device_info_by_host_api_device_index(0, device_out) if device_out else MAX_CHANNELS
    channels = min(channels_in, channels_out, MAX_CHANNELS)
    frames_per_buffer = CHUNK * channels

    stream_in = p.open(
            rate = RATE,
            channels = channels,
            format = FORMAT,
            input = True,
            input_device_index = device_in,
            frames_per_buffer = frames_per_buffer
        )
    stream_out = p.open(
            rate = RATE,
            channels = channels,
            format = FORMAT,
            output = True,
            output_device_index = device_in,
            frames_per_buffer = frames_per_buffer
        )

    # Alternatively, can be implemented with callbacks
    while True:
        data = stream_in.read(frames_per_buffer)
        stream_out.write(data)

def listdevices():
    import pyaudio
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    # Input devices
    print("DEVICES IN:")
    for i in range(0, numdevices):
        device_i = p.get_device_info_by_host_api_device_index(0, i)
        if (device_i.get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", device_i.get('name'))
    # Output devices
    print("DEVICES OUT:")
    for i in range(0, numdevices):
        device_i = p.get_device_info_by_host_api_device_index(0, i)
        if (device_i.get('maxOutputChannels')) > 0:
            print("Output Device id ", i, " - ", device_i.get('name'))
    p.terminate()



if __name__ == '__main__':
    listdevices()
    print("\nTurn on your speakers\nStart talking into your microphone")
    passthrough()