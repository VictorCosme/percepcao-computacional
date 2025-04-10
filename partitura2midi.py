import json
from mido import Message, MidiFile, MidiTrack, MetaMessage


def solfege_to_midi(note, octave):
    """Recebe uma nota musical e a oitava e retorna o número MIDI."""
    res = None
    pitch_map = {
        "Do": 0, "Do#": 1, 
        "Re": 2, "Re#": 3, 
        "Mi": 4, 
        "Fa": 5, "Fa#": 6,
        "Sol": 7, "Sol#": 8, 
        "La": 9, "La#": 10, 
        "Si": 11
    }
    if note != "  ":
        res = (octave + 1) * 12 + pitch_map[note]

    return res






mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)






musica = "bella_prova"
with open(f"partituras/{musica}.json", "r", encoding="utf-8") as f:
    melody = json.load(f)


duration_map = {
    "semibreve": 4,
    "minima": 2,
    "seminima": 1,
    "colcheia": 0.5,
    "semicolcheia": 0.25
}


# Configurar tempo
bpm = int(melody["tempo"])  # BPM como inteiro
ticks_per_beat = mid.ticks_per_beat
tempo = int(60_000_000 / bpm)  # Converte BPM para tempo em microssegundos
track.append(MetaMessage("set_tempo", tempo=tempo))

# Adicionando notas e pausas
for note in melody["notas"]:
    midi_number = solfege_to_midi(note["nota"], note["oitava"])
    duration_ticks = int(duration_map[note["duracao"]] * ticks_per_beat)

    if midi_number is None:
        # Se for uma pausa, apenas adiciona tempo sem um evento de nota
        track.append(Message("note_off", note=0, velocity=0, time=duration_ticks))
    else:
        track.append(Message("note_on", note=midi_number, velocity=64, time=0))
        track.append(Message("note_off", note=midi_number, velocity=64, time=duration_ticks))

# Salvando o arquivo MIDI
midi_filename = f"{musica}.mid"
mid.save(midi_filename)
print(f"MIDI salvo como {midi_filename}")
