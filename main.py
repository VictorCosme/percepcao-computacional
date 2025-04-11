import mido
import librosa
import librosa.display
import numpy as np
from mido import Message, MidiFile, MidiTrack
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
import tempfile


def main(partitura, delay, naipe):
    melodia = gerar_midi_temporario(partitura)
    notas_esperadas = get_notas_esperadas(partitura)
    num_divisoes = len(notas_esperadas)

    canto = executar_e_gravar(melodia, delay)
    #    canto = tratar_audio(canto, naipe)

    notas_cantadas = get_notas_cantadas(canto, num_divisoes)

    return avaliar_canto(notas_cantadas, notas_esperadas)


def gerar_midi_temporario(partitura):
    """
    Gera um arquivo MIDI temporário a partir de uma partitura em formato de dicionário.

    Args:
        partitura (dict): Dicionário com chaves "title", "tempo" e "notas".

    Returns:
        str: Caminho do arquivo .mid temporário gerado.
    """
    notas_midi = {
        "DO": 0, "DO#": 1, "RE": 2, "RE#": 3, "MI": 4, "FA": 5,
        "FA#": 6, "SOL": 7, "SOL#": 8, "LA": 9, "LA#": 10, "SI": 11
    }

    duracoes = {
        "semibreve": 1920,
        "minima": 960,
        "seminima": 480,
        "colcheia": 240,
        "semicolcheia": 120
    }

    mid = MidiFile(ticks_per_beat=480)
    track = MidiTrack()
    mid.tracks.append(track)

    bpm = int(partitura.get("tempo", 120))
    microseconds_per_beat = int(60_000_000 / bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

    for n in partitura["notas"]:
        nome = n["nota"].strip().upper()
        oitava = n["oitava"]
        dur = duracoes.get(n["duracao"], 480)

        if nome == "":
            track.append(Message('note_off', note=0, velocity=0, time=dur))
            continue

        nota_valor = notas_midi.get(nome)
        if nota_valor is None:
            print(f"Nota não reconhecida: {nome}")
            continue

        pitch = nota_valor + (oitava + 1) * 12
        track.append(Message('note_on', note=pitch, velocity=64, time=0))
        track.append(Message('note_off', note=pitch, velocity=64, time=dur))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mid")
    mid.save(temp_file.name)
    temp_file.close()

    return temp_file.name


def get_notas_esperadas(partitura):
    duracoes = {
        "semibreve": 1920,
        "minima": 960,
        "seminima": 480,
        "colcheia": 240,
        "semicolcheia": 120
    }

    # Inverter o dicionário para mapear ticks de volta para nomes
    duracoes_invertido = {v: k for k, v in duracoes.items()}

    # Encontrar a menor duração usada na partitura
    duracoes_usadas = [duracoes[n["duracao"]] for n in partitura["notas"]]
    menor_duracao = min(duracoes_usadas)

    # Criar nova lista de notas normalizadas
    notas_normalizadas = []
    for n in partitura["notas"]:
        d = duracoes[n["duracao"]]
        repeticoes = d // menor_duracao
        for _ in range(repeticoes):
            nota_clonada = {
                "nota": n["nota"],
                "oitava": n["oitava"],
                "duracao": duracoes_invertido[menor_duracao]
            }
            notas_normalizadas.append(nota_clonada)

    # Montar a nova partitura
    return notas_normalizadas


def executar_e_gravar(melodia, delay):
    """executa paralelamente os métodos executar_melodia() e
    capturar_audio()"""
    # executar(melodia, delay)
    canto = capturar_audio()
    return canto


def executar(melodia, delay):
    pass


def capturar_audio(duracao):
    fs = 44100  # Frequência de amostragem (CD quality)
    print(f"Gravando por {duracao} segundos...")

    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Espera a gravação terminar

    # Cria um arquivo temporário WAV
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_file.name, fs, audio)

    print(f"Gravação salva em: {temp_file.name}")
    return temp_file.name


def tratar_audio(audio, naipe):
    """corta e filtra o audio de acordo com as frequencias do naipe vocal"""
    pass


def get_notas_cantadas(audio, num_divisoes):
    """
    Analisa um arquivo de áudio e extrai as notas cantadas.
    """
    notas_cantadas = [
        get_nota(audio_slice)
        for audio_slice in slice(audio, num_divisoes)
    ]
    return notas_cantadas


def slice(audio, num_divisoes):
    """
    Divide um arquivo de áudio em um número especificado de segmentos de igual duração.
    """
    sr, data = wavfile.read(audio)

    if len(data.shape) > 1:
        data = data[:, 0]

    segment_size = len(data) // num_divisoes

    segments = []
    for i in range(num_divisoes):
        start = i * segment_size
        end = start + segment_size

        if i == num_divisoes - 1:
            segment = data[start:]
        else:
            segment = data[start:end]

        segments.append((segment, sr))

    return segments


def freq_to_note(freq):
    notas = ['do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']
    semitons = round(12 * np.log2(freq / 440.0))
    nota = notas[(semitons + 9) % 12]
    oitava = 4 + ((semitons + 9) // 12)

    return f"{nota}{oitava}".upper()


def get_nota(audio_slice):
    """
    Identifica a nota musical em um segmento de áudio.
    """
    audio_data, sr = audio_slice
    f0, voiced_flag, voiced_probs = librosa.pyin(
        audio_data,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr
    )

    f0_valid = f0[voiced_flag]
    if len(f0_valid) == 0:
        # Nenhuma frequência vozeada detectada (silêncio ou ruído)
        return {
            "nota": "",
            "oitava": 0,
            "duracao": "seminima"  # Duração padrão
        }

    mediana = np.median(f0_valid) if len(f0_valid) > 0 else None
    if mediana <= 0:
        return {
            "nota": "",
            "oitava": 0,
            "duracao": "seminima"
        }

    notas = ['DO', 'DO#', 'RE', 'RE#', 'MI', 'FA', 'FA#', 'SOL', 'SOL#', 'LA', 'LA#', 'SI']
    semitons = round(12 * np.log2(mediana / 440.0))
    nota = notas[(semitons + 9) % 12].upper()
    oitava = 4 + ((semitons + 9) // 12)

    duracao = "seminima"
    # como analisar e definir a duração do slice?

    return {
        "nota": nota,
        "oitava": oitava,
        "duracao": duracao
    }


def avaliar_canto(notas_cantadas, notas_esperadas):
    if len(notas_cantadas) != len(notas_esperadas):
        print("esperava-se notas_cantadas == notas_esperadas...")

    acertos = 0

    for cantada, esperada in zip(notas_cantadas, notas_esperadas):
        if cantada == esperada:
            acertos += 1

    score = acertos / len(notas_esperadas)

    return score


if __name__ == '__main__':
    partitura = {"title": "Bella prova è d'alma forte",
                 "tempo": "85",
                 "notas": [
                     {"nota": "DO", "oitava": 4, "duracao": "seminima"},
                     {"nota": "DO", "oitava": 4, "duracao": "semicolcheia"},
                     {"nota": "  ", "oitava": 4, "duracao": "semicolcheia"},
                     {"nota": "MI", "oitava": 4, "duracao": "seminima"},
                     {"nota": "MI", "oitava": 4, "duracao": "colcheia"},
                 ]}

    delay = None
    naipe = None

    res = capturar_audio(10)


    def reproduzir_audio(caminho_arquivo):
        fs, data = wavfile.read(caminho_arquivo)
        print("Reproduzindo...")
        sd.play(data, samplerate=fs)
        sd.wait()  # Espera terminar a reprodução
        print("Reprodução finalizada.")


    reproduzir_audio(res)
