import librosa
import librosa.display
import numpy as np


def freq_para_nota(freq):
    if freq <= 0:
        return None
    notas = ['do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']
    semitons = round(12 * np.log2(freq / 440.0))
    nota = notas[(semitons + 9) % 12]
    oitava = 4 + ((semitons + 9) // 12)

    return f"{nota}{oitava}"


arquivos = ["Do#4", "Do4", "Fa#4"]

for arquivo in arquivos:
    y, sr = librosa.load(f"{arquivo}.wav")
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr
    )

    print(f"nota: {arquivo}")
    f0_valido = f0[voiced_flag]
    mediana = np.median(f0_valido) if len(f0_valido) > 0 else None
    print(f"mediana: {mediana}, {freq_para_nota(mediana)}")
    print()

