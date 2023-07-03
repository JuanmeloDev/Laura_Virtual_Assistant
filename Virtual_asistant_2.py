import spoty
import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime, date, timedelta
import pyjokes
from time import time


start_time = time()
engine = pyttsx3.init()

# name of the virtual assistant
name = 'Laura'

# Personal Spotify credentials
client_id = 'aea3fbf1f0554dc598dd77b88f30a012'
client_secret = 'c58898c782d14880802b46d32fc81e64'


# colors
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

# get voices and set the first of them
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

day_es = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", 
          "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
day_en = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
          "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

def getDaysAgo(rec):
    value =""
    if 'ayer' in rec:
        days = 1
        value = 'ayer'
    elif 'antier' in rec:
        days = 2
        value = 'antier'
    else:
        rec = rec.replace(",","")
        rec = rec.split()
        days = 0

        for i in range(len(rec)):
            try:
                days = float(rec[i])
                break
            except:
                pass
    
    if days != 0:
        try:
            now = date.today() - timedelta(days=days)
            now = now.strftime("%A, %d de %B del %Y").lower()

            if value != "":
                return f"{value} fue {iterateDays(now)}"
            else:
                return f"Hace {days} días fue {iterateDays(now)}"
        except:
            return "Aún no existíamos"
    else:
        return "No entendí"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
   
    with sr.Microphone() as source:
        print(f"{green_color}Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            
            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return rec

while True:
    rec = get_audio()

    if 'estas ahi' in rec:
        speak('Por supuesto')

    elif 'reproduce' in rec:
        if 'spotify' in rec:
            music = rec.replace('reproduce en spotify', '')
            speak(f'Reproduciendo {music}')
            spoty.play(client_id, client_secret, music)
        else:
            music = rec.replace('reproduce', '')
            speak(f'Reproduciendo {music}')
            pywhatkit.playonyt(music)
    elif 'que' in rec:
        if 'hora' in rec:
            hora = datetime.now().strftime('%I:%M %p')
            speak(f"Son las {hora}")

        elif 'dia' in rec:
            if 'fue' in rec:
                speak(f"{getDaysAgo(rec)}")
            else:
                speak(f"Hoy es {getDay()}")
    elif 'chiste' in rec:
        chiste = pyjokes.get_joke("es")
        speak(chiste)
    elif 'descansa' in rec:
        speak("Saliendo...")
        break
print(f"{red_color} PROGRAMA FINALIZADO CON UNA DURACIÓN DE: { int(time() - start_time) } SEGUNDOS {normal_color}")