import sounddevice as sd
import numpy as np
import librosa
import noisereduce as nr
import math

SR = 44100  # Taxa de amostragem
DURACAO = 2  # Duração da gravação em segundos
NOTAS_REF = ['do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']

# Grava ruído ambiente para referência
def gravar_ruido(duracao=4):
    print("Gravando ruído de fundo... Fique em silêncio")
    ruido = sd.rec(int(duracao * SR), samplerate=SR, channels=1, dtype='float32')
    sd.wait()
    return ruido.flatten()

# Grava áudio com a pessoa cantando
def gravar_audio(duracao=DURACAO):
    print("Agora cante uma nota...")
    audio = sd.rec(int(duracao * SR), samplerate=SR, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten()

# Reduz ruído usando noisereduce
def reduzir_ruido(audio, ruido):
    return nr.reduce_noise(y=audio, y_noise=ruido, sr=SR)

# Detecta pitch médio usando Librosa
def detectar_pitch(audio):
    # pitches, magnitudes = librosa.piptrack(y=audio, sr=SR)
    # pitch_vals = [pitches[:, t].max() for t in range(pitches.shape[1]) if pitches[:, t].max() > 0]
    # return np.mean(pitch_vals) if pitch_vals else 0
    f0, tem_voz, _ = librosa.pyin(
        audio,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=SR)
    f0_valido = f0[~np.isnan(f0)]
    return np.mean(f0_valido) if len(f0_valido) > 0 else 0

# Converte frequência para nome da nota musical
def freq_para_nota(freq):
    if freq <= 0:
        return None
    semitons = round(12 * math.log2(freq / 440.0))
    nota = NOTAS_REF[(semitons + 9) % 12]  # +9 para alinhar com A4=440Hz
    oitava = 4 + ((semitons + 9) // 12)
    return f"{nota}{oitava}"

# Programa principal
def main():
    ruido = gravar_ruido()

    while True:
        audio = gravar_audio()
        audio_limpo = reduzir_ruido(audio, ruido)
        audio_normalizado = librosa.util.normalize(audio_limpo)
        freq = detectar_pitch(audio_normalizado)

        nota = freq_para_nota(freq)
        if nota:
            print(f"Nota detectada: {nota} (Frequência: {freq:.2f} Hz)")
        else:
            print("Não foi possível detectar uma nota com precisão.")
    

if __name__ == "__main__":
    main()