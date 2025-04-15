import sounddevice as sd
from scipy.io.wavfile import write

def capturar_audio(nome_arquivo, duracao=None):
    fs = 44100  # Frequência de amostragem (CD quality)

    print(f"Gravando por {duracao} segundos...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Espera a gravação terminar

    write(nome_arquivo, fs, audio)
    print(f"Gravação salva em: {nome_arquivo}")

    return nome_arquivo
