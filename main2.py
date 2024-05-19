from customtkinter import *
from PIL import Image
import time as t
from bird_model import classify_audio
from threading import Thread, Event
import pyaudio
import wave
from record_bird import list_audio_devices
import numpy as np
from dirt_model import run_model
import pathlib
import math


file = (str(pathlib.Path(__file__).parent.resolve())+"/images/")
modelFiles = (str(pathlib.Path(__file__).parent.resolve())+"/models/")

# Initialize the main application window
app = CTk()
app.geometry("1920x1080")
app.title("The Environmentalist's Handbook")
set_appearance_mode("dark")

# Load images
bgIMG1 = Image.open(file + "mountain_bg.png")
bgIMG2 = Image.open(file + "rocky_mountain_bg.png")
background_image = CTkImage(bgIMG1, size=(1920, 1080))
background_image2 = CTkImage(bgIMG2, size=(1920, 1080))

bg_lbl2 = CTkLabel(app, text="", image=background_image2)
bg_lbl2.place(x=1200, y=800, anchor="center")

bg_lbl1 = CTkLabel(app, text="", image=background_image)
bg_lbl1.place(x=-100, y=800, anchor="center")
leafIMG = Image.open(file + "green_leaf.png")

# Load fonts
terminal_font = CTkFont(family="Terminal", size=40)
terminal_font_small = CTkFont(family="Terminal", size=20)
jokerman_font = CTkFont(family="Jokerman", size=80)
jokerman_font_large = CTkFont(family="Jokerman", size=240)
credit_font = CTkFont(family="Agency FB", size=30)
credit_font_large = CTkFont(family="Agency FB", size=50)

# Define UI elements and their functions
def begin():
    openHandbook.destroy()
    splashLabel.destroy()
    splashCredits1.destroy()
    splashCredits2.destroy()
    bg_lbl1.destroy()
    bg_lbl2.destroy()
    openTools()


openHandbook = CTkButton(
    master=app, 
    text="Open the Handbook!",
    corner_radius=30,
    fg_color="#36f569", 
    hover_color="#26ad31", 
    border_color="#665202", 
    border_width=5,
    width=800,
    height=180,
    image=CTkImage(dark_image=leafIMG, size=(70,70)),
    text_color="#24382a",
    font=terminal_font,
    command=begin
)

splashLabel = CTkLabel(
    master=app,
    text="Environmentalist's Handbook!",
    font=jokerman_font
)

splashCredits1 = CTkLabel(
    master=app,
    text="Samuel F.",
    font=credit_font
)
splashCredits2 = CTkLabel(
    master=app,
    text="Aden B.",
    font=credit_font
)

splashLabel.place(relx=0.5, rely=0.2, anchor="center")
splashCredits1.place(relx=0.51, rely=0.98, anchor="center")
splashCredits2.place(relx=0.51, rely=0.92, anchor="center")
openHandbook.place(relx=0.5, rely=0.5, anchor="center")

highestBird = 0

questionMarkLbl = CTkLabel(app, text="?", font=jokerman_font_large)

canaryIMG = Image.open(file + "canary.png")
canaryImage = CTkImage(canaryIMG, size=(300, 300))
canaryLbl = CTkLabel(app, text="", image=canaryImage)

crowIMG = Image.open(file + "crow.png")
crowImage = CTkImage(crowIMG, size=(300, 280))
crowLbl = CTkLabel(app, text="", image=crowImage)

owlIMG = Image.open(file + "owl.png")
owlImage = CTkImage(owlIMG, size=(200, 301))
owlLbl = CTkLabel(app, text="", image=owlImage)

finchIMG = Image.open(file + "finch.png")
finchImage = CTkImage(finchIMG, size=(300, 211))
finchLbl = CTkLabel(app, text="", image=finchImage)

mallardIMG = Image.open(file + "mallard.png")
mallardImage = CTkImage(mallardIMG, size=(300, 211))
mallardLbl = CTkLabel(app, text="", image=mallardImage)

seagullIMG = Image.open(file + "seagull.png")
seagullImage = CTkImage(seagullIMG, size=(300, 176))
seagullLbl = CTkLabel(app, text="", image=seagullImage)

birdLabel = CTkLabel(
    master=app,
    text="Listening...",
    font=credit_font_large
)

# Event object to signal when to stop listening
stop_event = Event()

def birdClose():
    global stop_event

    stop_event.set()
    birdListen.place_forget()
    combobox.place_forget()
    comboboxLabel.place_forget()
    birdBack.place_forget()
    ring.place_forget()
    birdLabel.place_forget()
    if listenThread.is_alive():
        listenThread.join()
    openTools()
    forget_birds()

def listen():
    global stop_event, highestBird

    highestBird = 0
    stop_event.clear()
    listenOutputs = [-100000,0,0,0,0,0,0]
    index = 0
    birdLabel.place(relx=0.35, rely=0.005)
    birdLabel.configure(text="Listening...")
    
    while not stop_event.is_set():
        record_audio("recording.wav", duration=1)
        result = classify_audio("recording.wav", modelFiles + "bird_classifier.tflite", modelFiles + "bird_labels.txt")
        listenOutputs[int(result[0])] += 1
        highestBird = listenOutputs.index(max(listenOutputs))
        print(listenOutputs)

        if index > 4:
            forget_birds()
            birdLabel.configure(text=f"Detected: {['Unknown', 'Canary', 'Crow', 'Owl', 'Finch', 'Mallard', 'Seagull'][highestBird]}")
            if highestBird == 0:
                questionMarkLbl.place(x=760, y=325, anchor='center')
            else:
                birdImages = [canaryLbl, crowLbl, owlLbl, finchLbl, mallardLbl, seagullLbl]
                birdImages[highestBird - 1].place(x=760, y=325, anchor='center')
            break
        index += 1

def forget_birds():
    questionMarkLbl.place_forget()
    canaryLbl.place_forget()
    crowLbl.place_forget()
    owlLbl.place_forget()
    finchLbl.place_forget()
    mallardLbl.place_forget()
    seagullLbl.place_forget()


def openTools():


    
    openBird.place(relx=0.2, rely=0.1)
    soilCheck.place(relx=0.6, rely=0.1)

def beginListenThread():
    global stop_event, listenThread
    stop_event.clear()
    listenThread = Thread(target=listen)
    listenThread.start()

listenThread = Thread(target=listen)

def openBirdApp():
    soilCheck.place_forget()
    openBird.place_forget()
    birdListen.place(anchor='center', relx=0.5, rely=0.8)
    combobox.place(relx=0.65, rely=0.9)
    comboboxLabel.place(relx=0.7, rely=0.85)
    birdBack.place(anchor='center', relx=0.1, rely=0.8)
    ring.place(relx=0.3, y=20)
    ring.lower()

birdImg = Image.open(file + "bird_logo.png")
CTkBirdImg = CTkImage(birdImg, size=(170,250))

dirtPileImage = Image.open(file + "dirt_pile.png")
CTkDirtImage = CTkImage(dirtPileImage, size=(300,150))

birdListenImage = Image.open(file + "listen.png")
CTkListen = CTkImage(birdListenImage, size=(50,50))

openBird = CTkButton(
    master=app,
    text="",
    corner_radius=30,
    fg_color="#0eabc7", 
    hover_color="#3cc6de", 
    border_color="#025563", 
    border_width=5,
    width=300,
    height=300,
    image=CTkBirdImg,
    text_color="#24382a",
    font=terminal_font,
    command=openBirdApp
)

birdListen = CTkButton(
    master=app,
    text="Listen...",
    corner_radius=20,
    fg_color="#09de49",
    hover_color="#20fa62", 
    border_color="#01541a",
    border_width=3,
    height=100,
    width=200,
    image=CTkListen,
    text_color="#000000",
    font=terminal_font,
    command=beginListenThread
)

birdBack = CTkButton(
    master=app,
    text="← Back",
    corner_radius=20,
    fg_color="#09de49",
    hover_color="#20fa62", 
    border_color="#01541a",
    border_width=3,
    height=100,
    width=200,
    text_color="#000000",
    font=terminal_font,
    command=birdClose
)


def openSoil():
    shift = 0.05

    soilCheck.place_forget()
    openBird.place_forget()
    nitrogenEntry.place(relx=shift+0.15,rely=0.7, anchor='center')
    phEntry.place(relx=shift+0.3,rely=0.7, anchor='center')
    ECEntry.place(relx=shift+0.45,rely=0.7, anchor='center')
    zincEntry.place(relx=shift+0.6,rely=0.7, anchor='center')
    ironEntry.place(relx=shift+0.75,rely=0.7, anchor='center')
    soilCalculate.place(relx=0.5, rely=0.85, anchor='center')
    soilLabel.place(relx=0.5, rely=0.2, anchor='center')
    soilElab.place(relx=0.5, rely=0.35, anchor='center')
    soilBack.place(relx=0.1, rely=0.85, anchor='center')
    
def calculateSoil():
    output = run_model(float(nitrogenEntry.get()), float(phEntry.get()), float(ECEntry.get()), float(zincEntry.get()), float(ironEntry.get()))[0]

    soilLabel.configure(text = output)
    if output < 0:
        soilElab.configure(text="Very Poor Soil")
    elif round(output) == 0:
        soilElab.configure(text="Poor Soil")
    elif round(output) == 1:
        soilElab.configure(text="Moderately Fertile Soil")
    elif round(output) == 2:
        soilElab.configure(text="Very Fertile Soil")
    else:
        soilElab.configure(text="Extremely Fertile Soil")
    
        
    
    



def closeSoil():
    nitrogenEntry.place_forget()
    phEntry.place_forget()
    ECEntry.place_forget()
    zincEntry.place_forget()
    ironEntry.place_forget()
    soilCalculate.place_forget()
    soilLabel.place_forget()
    soilElab.place_forget()
    soilBack.place_forget()

    openTools()

soilLabel = CTkLabel(
        app,
        text = 'Click "Calculate"',
        font = terminal_font
)
soilElab = CTkLabel(
        app,
        text = '',
        font = terminal_font
)

nitrogenEntry = CTkEntry(
        app, 
        placeholder_text="Nitrogen (PPM)",
        width=150,
        height=40
    )
phEntry = CTkEntry(
        app, 
        placeholder_text="pH Level",
        width=150,
        height=40
    )
ECEntry = CTkEntry(
        app, 
        placeholder_text="Electrical Conductivity",
        width=150,
        height=40
    )

zincEntry = CTkEntry(
        app, 
        placeholder_text="Zinc (PPM)",
        width=150,
        height=40
    )
ironEntry = CTkEntry(
        app, 
        placeholder_text="Iron (PPM)",
        width=150,
        height=40
    )

soilCalculate = CTkButton(
    master=app,
    text="Calculate",
    corner_radius=20,
    fg_color="#09de49",
    hover_color="#20fa62", 
    border_color="#01541a",
    border_width=3,
    height=100,
    width=200,
    text_color="#000000",
    font=terminal_font,
    command=calculateSoil
)

soilBack = CTkButton(
    master=app,
    text="Back",
    corner_radius=20,
    fg_color="#09de49",
    hover_color="#20fa62", 
    border_color="#01541a",
    border_width=3,
    height=100,
    width=200,
    text_color="#000000",
    font=terminal_font,
    command=closeSoil
)



soilCheck = CTkButton(
    master=app,
    text="",
    corner_radius=30,
    fg_color="#0eabc7", 
    hover_color="#3cc6de", 
    border_color="#025563", 
    border_width=5,
    width=300,
    height=300,
    image=CTkDirtImage,
    text_color="#24382a",
    font=terminal_font,
    command=openSoil
)



fishIMG = Image.open(file + "fish.png")
CTkFishImage = CTkImage(fishIMG, size=(300, 280))

def openFish():
    print()

fishCheck = CTkButton(
    master=app,
    text="",    
    corner_radius=30,
    fg_color="#0eabc7", 
    hover_color="#3cc6de", 
    border_color="#025563", 
    border_width=5,
    width=300,
    height=300,
    image=CTkFishImage,
    text_color="#24382a",
    command=openFish

)


index = 0

def record_audio(file_name, duration=1, rate=44100, chunk=1024, format=pyaudio.paInt16, channels=1, amplification_factor=1.0, device_index=index):
    audio = pyaudio.PyAudio()
    if device_index is None:
        device_index = audio.get_default_input_device_info()['index']
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, input_device_index=device_index, frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_data = np.clip(audio_data * amplification_factor, -32768, 32767).astype(np.int16)
    amplified_frames = audio_data.tobytes()

    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(rate)
    wave_file.writeframes(amplified_frames)
    wave_file.close()

    print(f"Audio saved as {file_name} with amplification factor {amplification_factor}")

index = 0
options = []
audio_devices = list_audio_devices()

def combobox_callback(choice):
    global index
    if choice[1] != ':':
        index = choice[:2]
    else:
        index = choice[0]
    print(index)

for index, name in audio_devices:
    options.append(f"{index}: {name}")

combobox = CTkComboBox(
    master=app,
    values=options,
    width=400,
    height=50,
    command=combobox_callback
)
comboboxLabel = CTkLabel(
    master=app,
    text='Select An Audio Input',
    font=terminal_font_small
)
combobox.set(options[0])

ringImage = Image.open(file + "ring.png")
CTkRingImage = CTkImage(ringImage, size=(600,600))

ring = CTkLabel(
    master=app,
    image=CTkRingImage,
    text=""
)

app.mainloop()
