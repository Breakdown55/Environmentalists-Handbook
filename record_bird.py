import pyaudio
import wave
import numpy as np

index = 0


def list_audio_devices():
    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()
    devices = []

    for i in range(device_count):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            devices.append((i, device_info['name']))
    
    audio.terminate()
    return devices


def changeIndex(device_index):
    global index

    index = device_index

