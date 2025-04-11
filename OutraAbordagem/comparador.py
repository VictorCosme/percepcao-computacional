"""
Módulo responsável por:
Comparar cada nota cantada com a esperada
Avaliar se a duração e afinação estão em uma margem aceitável
"""

from processador_partitura import *


def comparar_nota_cantada(prevista, detectada, tolerancia=1):
    if detectada is None:
        return False

    if (detectada["nota"] == "rest") != (prevista["nota"] == "rest"):
        return False

    if detectada["nota"] == prevista["nota"]:
        return True

    midi_prevista = solfejo_para_midi(prevista["nota"])
    midi_detectada = solfejo_para_midi(detectada["nota"])

    return abs(midi_prevista - midi_detectada) <= tolerancia  # tolerância padrão de ±1 semitom


def comparar_duracao(prevista, detectada, tolerancia=0.25):
    if detectada is None:
        return False

    if detectada["duracao"] == prevista["duracao"]:
        return True

    return abs(prevista["duracao"] - detectada["duracao"]) / prevista["duracao"] <= tolerancia


def avaliar_execucao(previstas, detectadas):
    avaliacao = []

    for prevista, detectada in zip(previstas, detectadas):
        afinacao_certa = comparar_nota_cantada(prevista, detectada)
        duracao_certa = comparar_duracao(prevista, detectada)

        avaliacao.append({
            "nota_esperada": prevista["nota"],
            "nota_detectada": detectada["nota"],
            "afinacao_certa": afinacao_certa,
            "duracao_certa": duracao_certa
        })

    return avaliacao
