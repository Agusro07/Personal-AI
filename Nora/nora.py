# nora_ligero_gpt4all.py
from gpt4all import GPT4All
import speech_recognition as sr
import os
import webbrowser
import json
import sys

# =====================
# 1️⃣ Cargar modelo ligero GPT4All
# =====================
try:
    # Reemplaza con la ruta de tu modelo ligero en español, ej: "ggml-modelo-espanol-pequeño.bin"
    nora = GPT4All("ggml-modelo-espanol-pequeño.bin")
except Exception as e:
    print("Error cargando el modelo ligero:", e)
    sys.exit(1)

# =====================
# 2️⃣ Funciones de notas
# =====================
ARCHIVO_NOTAS = "notas.json"

def guardar_nota(nota):
    try:
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            notas = json.load(f)
    except FileNotFoundError:
        notas = []
    notas.append(nota)
    with open(ARCHIVO_NOTAS, "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

def mostrar_notas():
    try:
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            notas = json.load(f)
        return "\n".join(f"- {n}" for n in notas) if notas else "No hay notas guardadas."
    except FileNotFoundError:
        return "No hay notas guardadas."

# =====================
# 3️⃣ Funciones de sistema
# =====================
def abrir_programa(ruta_programa):
    if os.path.exists(ruta_programa):
        try:
            if sys.platform.startswith("win"):
                os.startfile(ruta_programa)
            elif sys.platform.startswith("linux"):
                os.system(f'xdg-open "{ruta_programa}"')
            elif sys.platform.startswith("darwin"):
                os.system(f'open "{ruta_programa}"')
            else:
                return "Plataforma no soportada."
            return f"Abriendo {ruta_programa}"
        except Exception as e:
            return f"No se pudo abrir el programa: {e}"
    else:
        return "No encontré el programa."

def buscar_en_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Buscando '{query}' en Google..."

# =====================
# 4️⃣ Función de voz
# =====================
def escuchar_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Tú (voz):", texto)
        return texto
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        return ""
    except sr.RequestError as e:
        print("Error en el reconocimiento de voz:", e)
        return ""

# =====================
# 5️⃣ Función de respuesta GPT4All
# =====================
def generar_respuesta(comando):
    try:
        respuesta = nora.generate(comando)
        if isinstance(respuesta, list):
            return respuesta[0]
        return str(respuesta)
    except Exception as e:
        return f"Error generando respuesta: {e}"

# =====================
# 6️⃣ Loop principal
# =====================
def main():
    print("Nora ligera lista. (Ctrl+C para salir)")
    while True:
        try:
            comando = escuchar_comando()
            if comando.strip() == "":
                continue

            comando_lower = comando.lower()

            if "recordar" in comando_lower:
                nota = comando_lower.replace("recordar", "").strip()
                guardar_nota(nota)
                respuesta = f"Ok, lo recordaré: {nota}"
            elif "mostrar notas" in comando_lower:
                respuesta = mostrar_notas()
            elif "abrir programa" in comando_lower:
                ruta = comando_lower.replace("abrir programa", "").strip()
                respuesta = abrir_programa(ruta)
            elif "buscar" in comando_lower:
                query = comando_lower.replace("buscar", "").strip()
                respuesta = buscar_en_google(query)
            else:
                respuesta = generar_respuesta(comando)

            print("Nora:", respuesta)

        except KeyboardInterrupt:
            print("\nChau 👋")
            break
        except Exception as e:
            print("Ocurrió un error:", e)

# =====================
# 7️⃣ Ejecutar
# =====================
if __name__ == "__main__":
    main()
