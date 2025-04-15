"""
Módulo responsável por:
Comparar cada nota cantada com a esperada
Avaliar se a duração e afinação estão em uma margem aceitável
"""

from processador_partitura import *


def comparar_nota_cantada(prevista: dict[str, str | float],
                          detectada: dict[str, str | float],
                          tolerancia: int = 1) -> bool:

    if (detectada["nota"] == "rest") != (prevista["nota"] == "rest"):
        return False

    if detectada["nota"] == prevista["nota"]:
        return True

    midi_prevista = solfejo_para_midi(prevista["nota"])
    midi_detectada = solfejo_para_midi(detectada["nota"])

    return abs(midi_prevista - midi_detectada) <= tolerancia  # tolerância padrão de ±1 semitom


def comparar_duracao(prevista: dict[str, str | float],
                     detectada: dict[str, str | float],
                     tolerancia: float = 0.15) -> bool:

    if detectada["duracao"] == prevista["duracao"]:
        return True

    return abs(prevista["duracao"] - detectada["duracao"]) / prevista["duracao"] <= tolerancia


def avaliar_execucao(previstas: list[dict[str, str | float]] | None,
                     detectadas: list[dict[str, str | float]] | None,
                     tolerancia_afinacao: int = 1,
                     tolerancia_duracao: float = 0.25) -> list[dict[str, str | bool]]:

    print(f"Comparando e gerando o feedback...")

    if previstas is None or detectadas is None:
        return []

    avaliacao = []
    for prevista, detectada in zip(previstas, detectadas):
        afinacao_certa = comparar_nota_cantada(prevista, detectada, tolerancia_afinacao)
        duracao_certa = comparar_duracao(prevista, detectada, tolerancia_duracao)

        avaliacao.append({
            "nota_esperada": prevista["nota"],
            "nota_detectada": detectada["nota"],
            "afinacao_certa": afinacao_certa,
            "duracao_certa": duracao_certa
        })

    return avaliacao
