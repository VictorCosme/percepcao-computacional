"""
Módulo responsável por:
Processar a partitura JSON
Extrair as notas presentes na partitura, descartante pausas iniciais e finais
"""

import os
import json


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


def extrair_notas_json(melodia: dict) -> tuple[list[dict], float]:
    """
    Recebe um arquivo JSON e retorna uma lista com os eventos (notas e silêncios) presentes.
    """
    bpm = int(melodia["tempo"])
    tempo_seg = 60 / bpm

    mapa_duracoes = {
        "semibreve": 4,
        "minima": 2,
        "seminima": 1,
        "colcheia": 0.5,
        "semicolcheia": 0.25
    }

    eventos = []
    tempo_atual = 0
    precisao = 3

    for nota in melodia["notes"]:
        pitch = nota["pitch"]
        duracao = nota["duration"]
        duracao_seg = mapa_duracoes[duracao] * tempo_seg

        eventos.append({
            "nota": pitch,
            "inicio": round(tempo_atual, precisao),
            "duracao": round(duracao_seg, precisao)
        })

        tempo_atual += duracao_seg

    while eventos and eventos[0]["nota"] == "rest":
        eventos.pop(0)

    while eventos and eventos[-1]["nota"] == "rest":
        eventos.pop()

    duracao_minima = 0
    if eventos:
        deslocamento = eventos[0]["inicio"]
        for evento in eventos:
            evento["inicio"] = round(evento["inicio"] - deslocamento, precisao)

        duracao_minima = eventos[-1]["inicio"] + eventos[-1]["duracao"]

    return eventos, round(duracao_minima, precisao)


def processar_partitura(arquivo_json: str) -> tuple[list[dict], float]:
    """
    Recebe o nome do arquivo JSON da partitura e processa o arquivo
    """
    
    print(f"Processando a partitura para a melodia {arquivo_json}...")

    if not arquivo_json.endswith(".json"):
        arquivo_json += ".json"

    with open(arquivo_json, "r", encoding="utf-8") as f:
        melodia = json.load(f)

    res = extrair_notas_json(melodia)

    print(f"Partitura processada com sucesso. Foram encontradas {len(res[0])} notas.")
    print(f"Duração necessária aproximada de {res[1]} seg.")
    print()

    return res
