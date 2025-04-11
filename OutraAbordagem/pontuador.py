"""
Módulo responsável por:
Calcular a pontuação total baseada nos acertos
Gerar um feedback textual ou visual simples
"""


def calcular_score(comparacoes, peso_afinacao=0.5, peso_duracao=0.5):
    if not comparacoes:
        return None

    total = len(comparacoes)
    afinacoes_corretas = 0
    duracoes_corretas = 0

    for comparacao in comparacoes:
        afinacoes_corretas += 1 if comparacao["afinacao_certa"] else 0
        duracoes_corretas += 1 if comparacao["duracao_certa"] else 0

    pontos_afinacao = (afinacoes_corretas / total) * peso_afinacao
    pontos_duracao = (duracoes_corretas / total) * peso_duracao

    return round((pontos_afinacao + pontos_duracao) * 100, 2)


def gerar_feedback(comparacoes):
    if not comparacoes:
        return "Nenhuma nota a ser analisada."

    total = len(comparacoes)
    afinacoes_corretas = sum(1 for c in comparacoes if c["afinacao_certa"])
    duracoes_corretas = sum(1 for c in comparacoes if c["duracao_certa"])
    ambas_certas = sum(1 for c in comparacoes if c["afinacao_certa"] and c["duracao_certa"])

    afinacao_porcentagem = afinacoes_corretas / total
    duracao_porcentagem = duracoes_corretas / total
    acerto_total_porcentagem = ambas_certas / total

    feedback = (f"Das {total} notas, você acertou {ambas_certas} notas completamente!\n"
                f"- Afinação: {round(afinacao_porcentagem * 100, 2)}%\n"
                f"- Duração: {round(duracao_porcentagem * 100, 2)}%\n"
                f"- Pontuação total: {calcular_score(comparacoes)}")

    return feedback
