# =========================================================
# Mini-Nora llamado Nora - versión explicada paso a paso
# =========================================================

# Importamos herramientas que Nora va a usar
import datetime   # Para saber la hora actual
import json       # Para guardar y leer notas en un archivo
import webbrowser # Para abrir páginas web como YouTube

# =========================================================
# 1️⃣ Función para procesar lo que el usuario escribe
# =========================================================
def procesar_comando(comando: str):
    # Convertimos todo a minúsculas para no depender de mayúsculas
    comando = comando.lower()

    # ---------------------------
    # Si el comando contiene la palabra "hora"
    # ---------------------------
    if "hora" in comando:
        # Llamamos a la herramienta "hora" para decir la hora
        return usar_herramienta("hora")

    # ---------------------------
    # Si el comando menciona "youtube"
    # ---------------------------
    elif "youtube" in comando:
        # Dividimos el texto donde está la palabra "youtube"
        palabras = comando.split("youtube")
        # Si hay algo escrito después de "youtube", lo usamos como búsqueda
        if len(palabras) > 1:
            query = palabras[1].strip()  # Quitamos espacios extra
            return usar_herramienta("youtube", {"query": query})
        # Si no hay búsqueda, abrimos YouTube normal
        return usar_herramienta("youtube")

    # ---------------------------
    # Si el comando indica que Nora debe recordar algo
    # ---------------------------
    elif "recorda" in comando or "recuerda" in comando:
        # Quitamos la palabra "recorda/recuerda" para quedarnos solo con la nota
        nota = comando.replace("recorda", "").replace("recuerda", "").strip()
        # Llamamos a la herramienta "recordar" para guardar la nota
        return usar_herramienta("recordar", {"nota": nota})

    # ---------------------------
    # Si el usuario quiere ver las notas guardadas
    # ---------------------------
    elif "que me recordaste" in comando:
        return usar_herramienta("mostrar_notas")

    # ---------------------------
    # Si Nora no entiende el comando
    # ---------------------------
    else:
        return "No entiendo ese comando todavía 🤔"


# =========================================================
# 2️⃣ Función para ejecutar acciones concretas ("herramientas")
# =========================================================
def usar_herramienta(nombre, params=None):
    # ---------------------------
    # Herramienta "hora"
    # ---------------------------
    if nombre == "hora":
        # Obtenemos la hora actual en formato HH:MM
        ahora = datetime.datetime.now().strftime("%H:%M")
        return f"Son las {ahora}"

    # ---------------------------
    # Herramienta "youtube"
    # ---------------------------
    elif nombre == "youtube":
        # Si hay parámetros, tomamos la búsqueda (query)
        query = params.get("query") if params else None
        url = "https://www.youtube.com"
        # Si hay búsqueda, construimos la URL de resultados
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        # Abrimos la página web
        webbrowser.open(url)
        return f"Abriendo YouTube {('de ' + query) if query else ''}"

    # ---------------------------
    # Herramienta "recordar"
    # ---------------------------
    elif nombre == "recordar":
        nota = params.get("nota", "")
        guardar_nota(nota)  # Guardamos la nota en el archivo JSON
        return f"Ok, lo recordaré: {nota}"

    # ---------------------------
    # Herramienta "mostrar_notas"
    # ---------------------------
    elif nombre == "mostrar_notas":
        notas = cargar_notas()  # Leemos las notas del archivo
        if not notas:  # Si no hay notas, avisamos
            return "No tengo nada guardado."
        # Si hay notas, las mostramos en una lista
        return "Notas guardadas:\n" + "\n".join(f"- {n}" for n in notas)

    # ---------------------------
    # Si la herramienta no existe
    # ---------------------------
    else:
        return "Herramienta no reconocida."


# =========================================================
# 3️⃣ Funciones para la "memoria" de Nora usando un archivo JSON
# =========================================================
ARCHIVO = "notas.json"  # Archivo donde se guardan las notas

# Guardar una nota nueva
def guardar_nota(nota: str):
    notas = cargar_notas()  # Leemos las notas actuales
    notas.append(nota)      # Agregamos la nueva nota
    # Guardamos todo de nuevo en el archivo JSON
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

# Leer todas las notas guardadas
def cargar_notas():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)  # Devolvemos las notas como lista
    except FileNotFoundError:
        # Si el archivo no existe todavía, devolvemos una lista vacía
        return []


# =========================================================
# 4️⃣ Loop principal - donde Nora "escucha" tus comandos
# =========================================================
def main():
    print("Nora base lista. Escribí tus comandos (Ctrl+C para salir).")
    while True:  # Bucle infinito para que Nora siga escuchando
        try:
            comando = input("\nTú: ")           # Espera que escribas algo
            respuesta = procesar_comando(comando)  # Procesa tu comando
            print("Nora:", respuesta)           # Muestra la respuesta
        except KeyboardInterrupt:
            # Si presionás Ctrl+C, salimos del programa
            print("\nChau 👋")
            break

# =========================================================
# Esto ejecuta el programa si abrís este archivo directamente
# =========================================================
if __name__ == "__main__":
    main()
