# utils.py
import subprocess
import json
import os
import speech_recognition as sr

# =====================
# Abrir programas
# =====================
def abrir_programa(nombre):
    """
    Abre un programa según el nombre dado.
    """
    nombre = nombre.lower()
    if "bloc" in nombre:
        subprocess.Popen(['notepad.exe'])
    elif "navegador" in nombre:
        subprocess.Popen(['start', 'chrome'], shell=True)
    else:
        print(f"No sé abrir {nombre}")

# =====================
# Funciones para notas
# =====================
ARCHIVO = "notas.json"

def guardar_nota(nota):
    notas = cargar_notas()
    notas.append(nota)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

def cargar_notas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# =====================
# Escuchar voz del usuario
# =====================
def escuchar_comando():
    """
    Escucha la voz del usuario y devuelve el texto.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Tú (voz):", texto)
        return texto
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        return ""
    except sr.RequestError as e:
        print("Error al conectarse al servicio de reconocimiento de voz:", e)
        return ""
