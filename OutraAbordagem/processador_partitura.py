"""
Módulo responsável por:
Converter o arquivo json em mid
Extrair as notas e durações do mid
"""

import json
from mido import Message, MidiFile, MidiTrack, MetaMessage


def solfejo_para_midi(nota: str) -> int | None:
    """
    Recebe uma nota musical acompanhada da oitava (ex. Mi#4) e retorna o número MIDI.
    """
    if nota == "rest":
        return None

    mapa_pitch = {
        "Do": 0, "Do#": 1,
        "Re": 2, "Re#": 3,
        "Mi": 4,
        "Fa": 5, "Fa#": 6,
        "Sol": 7, "Sol#": 8,
        "La": 9, "La#": 10,
        "Si": 11
    }

    nome_nota = nota[:-1]
    oitava = int(nota[-1])

    return (oitava + 1) * 12 + mapa_pitch[nome_nota]


def midi_para_solfejo(numero_midi: int) -> str:
    """
    Recebe o número MIDI e retorna uma nota musical acompanhada da oitava (ex. Mi#4).
    """
    notas = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    oitava = (numero_midi // 12) - 1
    nota = notas[numero_midi % 12]

    return f"{nota}{oitava}"


def json_para_midi(nome_arquivo_json):
    """
    Recebe o nome de um arquivo json e o converte para um arquivo MIDI.
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    with open(f"{nome_arquivo_json}.json", "r", encoding="utf-8") as f:
        melodia = json.load(f)

    bpm = int(melodia["tempo"])
    ticks_por_beat = mid.ticks_per_beat
    tempo = int(60_000_000 / bpm)
    track.append(MetaMessage("set_tempo", tempo=tempo))

    mapa_duracoes = {
        "semibreve": 4,
        "minima": 2,
        "seminima": 1,
        "colcheia": 0.5,
        "semicolcheia": 0.25
    }

    delay = 0
    for nota in melodia["notes"]:
        midi_number = solfejo_para_midi(nota["pitch"])
        duration_ticks = int(mapa_duracoes[nota["duration"]] * ticks_por_beat)

        if midi_number is None:
            track.append(Message("note_off", note=0, velocity=0, time=duration_ticks))
        else:
            track.append(Message("note_on", note=midi_number, velocity=64, time=0))
            track.append(Message("note_off", note=midi_number, velocity=64, time=duration_ticks))

    midi_filename = f"{nome_arquivo_json}.mid"
    mid.save(midi_filename)


def extrair_notas(nome_arquivo_midi):
    """
    Recebe um arquivo MIDI e retorna uma lista com os eventos (notas e silêncios) presentes.
    """
    if not nome_arquivo_midi.endswith(".mid"):
        nome_arquivo_midi += ".mid"

    mid = MidiFile(nome_arquivo_midi)
    ticks_por_beat = mid.ticks_per_beat
    tempo = 500_000

    eventos = []
    notas_ativas = {}
    tempo_atual = 0
    ultimo_fim = 0

    for msg in mid:
        tempo_atual += msg.time

        if msg.type == "set_tempo":
            tempo = msg.tempo

        if msg.type == "note_on" and msg.velocity > 0:
            notas_ativas[msg.note] = tempo_atual

        elif (msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0)) and msg.note in notas_ativas:
            inicio = notas_ativas.pop(msg.note)
            duracao = tempo_atual - inicio

            segundos_por_tick = tempo / (ticks_por_beat * 1_000)
            inicio_seg = inicio * segundos_por_tick
            duracao_seg = duracao * segundos_por_tick

            # detecção de pausas
            if inicio_seg > ultimo_fim:
                eventos.append({
                    "nota": "rest",
                    "inicio": ultimo_fim,
                    "duracao": round(inicio_seg - ultimo_fim, 3)
                })

            eventos.append({
                "nota": midi_para_solfejo(msg.note),
                "inicio": inicio_seg,
                "duracao": round(duracao_seg, 3)
            })

            ultimo_fim = inicio_seg + duracao_seg

    return eventos


def processar_partitura(nome_arquivo_json):
    """
    Recebe o nome do arquivo json da partitura e processa o arquivo
    """
    json_para_midi(nome_arquivo_json)
    return extrair_notas(f"{nome_arquivo_json}.mid")
