# Laboratorio-3-PDS
## OBJETIVO
Este laboratorio tiene como objetivo analizar,capturar, procesamiento y separación de señales de audio provenientes de múltiples fuentes en un entorno simulado, utilizando técnicas de análisis temporal y espectral, así como métodos de separación de fuentes como el Análisis de Componentes Independientes (ICA) o Beamforming, para aislar y evaluar la calidad de una señal de voz específica.
## Procedimiento
El presente laboratorio se divide en tres secciones principales, la configuracion del sistema, captura de la señal y procesamiento de las señales captudaradas.Cado proceso será explicado a fondo a continuación:
### Configuración del sistema 
Para capturar las señales sonoras se utilizaron tres microfonos distribuidos estratégicamente con la intención de que cada uno de ellos capture de diferentes maneras las señales sonoras de las fuentes que en este caso natural ya que proviene de los integrantes de este grupo y fueron distribuidos de la siguiente manera:
![IMG_0200](https://github.com/user-attachments/assets/665062e0-28bc-4e69-b991-c40ebb66e125)
Como especifica la imagen las fuentes son las x respectivamente donde la fuente A es saniago, la fuente B es felipe y la fuente c es karol ubicados a diferentes distancias para simular de forma correcta la fiesta de cóctel.
### Captura de la señal 
para capturar las señales las tres fuentes naturales generan la señal mediante la voces de las mismas en este caso al momento de capturar la señal se esperan 5 segundos para capturar el ruido de la habitación, posterior a esto cada uno empezo a emitir las señales para registrarlas en los micrófonos para ser guardadas y procesadas cabe resaltar que cada una de ellas fue capturada a una frecuencia de 44.100Hz posterior a esto se calcula el SNR de la siguiente manera:
```ruby
import numpy as np
import scipy.io.wavfile as wav
import os

# Ruta donde están los audios
ruta_audios = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3"

# Lista de archivos de audio
audios = ["audioc.wav", "audios.wav", "audiof.wav"]
audios = [os.path.join(ruta_audios, audio) for audio in audios]  # Construye la ruta completa

def calcular_snr(audio_path):
    # Leer el archivo de audio
    sample_rate, data = wav.read(audio_path)

    # Convertir a flotante si es necesario
    if data.dtype != np.float32:
        data = data.astype(np.float32)

    # Estimación del ruido: tomamos el primer 10% del audio
    ruido_estimado = data[:len(data) // 10]

    # Calcular la potencia de la señal y la del ruido
    potencia_senal = np.mean(data ** 2)
    potencia_ruido = np.mean(ruido_estimado ** 2)

    # Calcular el SNR en decibeles (dB)
    snr = 10 * np.log10(potencia_senal / potencia_ruido)

    return snr

# Procesar cada audio
for audio in audios:
    if os.path.exists(audio):  # Verificar si el archivo existe
        snr = calcular_snr(audio)
        print(f"SNR de {os.path.basename(audio)}: {snr:.2f} dB")
    else:
        print(f"El archivo {audio} no existe en la ruta especificada.")
```
Se utilizó la siguiente función = calcular_snr(audio_path):
- Esta lee el archivo .wav usando wav.read(), obteniendo la frecuencia de muestreo (sample_rate) y los datos de audio (data).
* Convierte los datos a np.float32 si no lo están, para asegurar cálculos precisos.
* Estima el ruido tomando el primer 10% del audio ( ya que al inicio hay 5 segundos de solo ruido).
* Calcula la potencia de la señal y del ruido usando la media del cuadrado de los valores.
* Finalmente calcula el SNR en decibeles (dB) usando la fórmula: 10 * log10(potencia_señal / potencia_ruido).\
Obteniendo los siguientes resultados:\
![WhatsApp Image 2025-03-06 at 8 38 40 PM](https://github.com/user-attachments/assets/152e006b-672a-43bf-98ab-0eb719923f84)
### Procesamiento de señales
Para analizar correctamente las señales se realiza un análisis temporal y espectral de las señales capturadas por cada micrófono respectivamente con la intención de identificar las características principales de cada fuente, estos fueron realizados de la siguiente manera:
```ruby
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Ruta donde están los archivos .wav
ruta_audios = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3"

# Lista de archivos de audio en formato .wav
audios_wav = ["audioc.wav", "audios.wav", "audiof.wav"]
audios_wav = [os.path.join(ruta_audios, audio) for audio in audios_wav]  # Construye la ruta completa

def analizar_audio(audio_path):
    """Realiza análisis temporal y espectral de un archivo .wav"""
    # Leer el archivo de audio
    sample_rate, data = wav.read(audio_path)

    # Convertir a flotante si es necesario
    if data.dtype != np.float32:
        data = data.astype(np.float32)

    # Si el audio tiene más de un canal (estéreo), convertirlo a mono
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)  # Promedio de canales

    # Duración del audio en segundos
    duracion = len(data) / sample_rate
    tiempo = np.linspace(0., duracion, len(data))

    # ---- ANÁLISIS TEMPORAL ----
    plt.figure(figsize=(12, 5))
    plt.plot(tiempo, data, label="Señal de audio", color="blue")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title(f"Análisis Temporal de {os.path.basename(audio_path)}")
    plt.legend()
    plt.grid()
    plt.show()

    # ---- ANÁLISIS ESPECTRAL (FFT) ----
    N = len(data)  # Número de muestras
    fft_senal = fft(data)  # Aplicar FFT
    freqs = fftfreq(N, 1 / sample_rate)  # Obtener frecuencias

    # Graficar solo la parte positiva del espectro
    plt.figure(figsize=(12, 5))
    plt.plot(freqs[:N // 2], np.abs(fft_senal[:N // 2]), label="Espectro de frecuencia", color="red")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    plt.title(f"Análisis Espectral (FFT) de {os.path.basename(audio_path)}")
    plt.legend()
    plt.grid()
    plt.show()

# Procesar cada archivo .wav
for audio_wav in audios_wav:
    if os.path.exists(audio_wav):  # Verificar si el archivo existe
        analizar_audio(audio_wav)  # Analizar señal
    else:
        print(f"El archivo {audio_wav} no existe en la ruta especificada.")
```
Se utilizó la función analizar_audio(audio_path) que se encarga de:
* Convierte a mono si es estéreo.
* Calcula la duración y el vector de tiempo.
* **Análisis temporal:** Crea una gráfica de la amplitud de la señal en función del tiempo.
* **Análisis espectral (FFT):**
* Se calcula la transformada rápida de fourier de la señal usando fft().
* Calcula las frecuencias correspondientes usando fftfreq().
* Crea una gráfica de la magnitud del espectro de frecuencia (solo la parte positiva) obteniendo los siguientes resultados:

