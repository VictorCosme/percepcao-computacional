import json
from mido import Message, MidiFile, MidiTrack, MetaMessage

from processador_partitura import solfejo_para_midi, json_para_midi


def main():
    musica = "bella_prova"
    json_para_midi(musica)


if __name__ == '__main__':
    main()
