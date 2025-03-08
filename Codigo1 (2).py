import numpy as np
import scipy.io.wavfile as wav
import os
from colorama import Fore, init
import soundfile as sf
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA
from scipy.fft import fft, fftfreq
from scipy.signal import resample, correlate

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

#PUNTO 3

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

#Beamforming
def calcular_retraso(distancias, velocidad, sr):
    return tuple(int(d / velocidad * sr) for d in distancias)

distancias = [2.5, 1.5, 1.32]  # Distancia entre micrófonos en metros
velocidad_sonido = 343  # Velocidad del sonido en m/s
sr1 = 44100
retraso = calcular_retraso(distancias, velocidad_sonido, sr1)

def beamforming(signals, delay):
    num_mics = signals.shape[1]
    beamformed_signal = np.zeros(len(signals))
    for i, delay_i in enumerate(delay):
        beamformed_signal += np.roll(signals[:, i], delay_i)
    return beamformed_signal / num_mics

# Asegurar que ambas señales tengan la misma longitud
audio1 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudioc.wav"
audio2 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudiof.wav"
audio3 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudios.wav"
sr1 = 44100
longitud_max = max(len(audio1), len(audio2), len(audio3))
audio1 = np.pad(audio1, (0, longitud_max - len(audio1)))
sample_rate, audio1 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudioc.wav")
audio2 = np.pad(audio2, (0, longitud_max - len(audio2)))
sample_rate, audio2 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudiof.wav")
audio3 = np.pad(audio3, (0, longitud_max - len(audio3)))
sample_rate, audio3 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\saudios.wav")
audio_mix = np.vstack((audio1, audio2, audio3)).T

# Aplicar beamforming
beamformed_signal = beamforming(audio_mix, retraso)
output_file = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\señal_beamformed.wav"
sf.write(output_file, beamformed_signal, sr1)

#graficar_señal
plt.figure(figsize=(12, 6))
plt.title('Señal después de Beamforming')
plt.plot(beamformed_signal, color='orange')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

#graficar_espectro
freqs = np.fft.rfftfreq(len(beamformed_signal), 1/sr1)
espectro = np.abs(np.fft.rfft(beamformed_signal))
plt.figure(figsize=(12, 6))
plt.title(f'Espectro de Señal Beamforming')
plt.plot(freqs, espectro, color='orange')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.show()

ruido1 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\ruidoc.wav" 
ruido2 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\ruidof.wav"
ruido3 = r"C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\ruidos.wav"

sample_rate, ruido1 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\audioc.wav")
sample_rate, ruido2 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\audiof.wav")
sample_rate, ruido3 = wav.read("C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\Lab 3\\audios.wav")

max_length = max(ruido1.shape[0], ruido2.shape[0], ruido3.shape[0])
ruido1 = np.pad(ruido1, ((0, max_length - ruido1.shape[0]), (0, 0)), mode='constant')
ruido2 = np.pad(ruido2, ((0, max_length - ruido2.shape[0]), (0, 0)), mode='constant')
ruido3 = np.pad(ruido3, ((0, max_length - ruido3.shape[0]), (0, 0)), mode='constant')

# Sumar las señales de ruido
señal_suma = ruido1 + ruido2 + ruido3

# Calcular SNR final
pseñal = np.mean(beamformed_signal[:max_length] ** 2)
pruido = np.mean(señal_suma ** 2)
print(pseñal)
print(pruido)
snrf = 10 * np.log10(pseñal / pruido)
print("SNR FINAL después de Beamforming:",snrf," dB")
