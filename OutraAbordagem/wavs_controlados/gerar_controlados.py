from mido import Message, MidiFile, MidiTrack, MetaMessage

from wavs_controlados.partitura2midi import solfege_to_midi

notas = ["Do4", "Do#4",
         "Re4", "Re#4", "Mi4",
         "Fa4", "Fa#4",
         "Sol4", "Sol#4",
         "La4", "La#4", "Si4"]

bpm = 120
tempo = int(60_000_000 / bpm)

for nota in notas:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage("set_tempo", tempo=tempo))

    midi_number = solfege_to_midi(nota)
    duration_ticks = mid.ticks_per_beat

    track.append(Message("note_on", note=midi_number, velocity=64, time=0))
    track.append(Message("note_off", note=midi_number, velocity=64, time=duration_ticks))

    midi_filename = f"{nota}.mid"
    mid.save(midi_filename)
    print(f"MIDI salvo como {midi_filename}")
