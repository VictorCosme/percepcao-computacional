import mido
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
    #executar(melodia, delay)
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
    notas_cantadas = [
        get_nota(audio_slice) 
        for audio_slice in slice(audio, num_divisoes)
    ]
    return notas_cantadas


def slice(audio, num_divisoes):
    pass


def get_nota(audio_slice):
    pass


def avaliar_canto(notas_cantadas, notas_esperadas):
    score = 0
    #todo
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
