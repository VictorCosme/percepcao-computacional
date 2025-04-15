"""
Módulo responsável por:
Calcular a pontuação total baseada nos acertos
Gerar um feedback textual ou visual simples
"""


def calcular_score(comparacoes, peso_afinacao=0.5):
    if not comparacoes:
        return None

    total = len(comparacoes)
    afinacoes_corretas = 0
    duracoes_corretas = 0

    for comparacao in comparacoes:
        afinacoes_corretas += 1 if comparacao["afinacao_certa"] else 0
        duracoes_corretas += 1 if comparacao["duracao_certa"] else 0

    pontos_afinacao = (afinacoes_corretas / total) * peso_afinacao
    pontos_duracao = (duracoes_corretas / total) * (1 - peso_afinacao)

    return round((pontos_afinacao + pontos_duracao) * 100, 2)


def gerar_feedback(comparacoes, peso_afinacao=0.5):
    if not comparacoes:
        return "Nenhuma nota a ser analisada."

    total = len(comparacoes)
    afinacoes_corretas = sum(1 for c in comparacoes if c["afinacao_certa"])
    duracoes_corretas = sum(1 for c in comparacoes if c["duracao_certa"])
    ambas_certas = sum(1 for c in comparacoes if c["afinacao_certa"] and c["duracao_certa"])

    afinacao_porcentagem = afinacoes_corretas / total
    duracao_porcentagem = duracoes_corretas / total
    score = calcular_score(comparacoes, peso_afinacao)

    if score < 10:
        emoji = "💀"
    elif score < 30:
        emoji = "❌"
    elif score < 50:
        emoji = "⚠️"
    elif score < 60:
        emoji = "😐"
    elif score < 70:
        emoji = "🙂"
    elif score < 80:
        emoji = "👍"
    elif score < 90:
        emoji = "🔥"
    else:
        emoji = "🏆"

    feedback = (f"Das {total} notas, você acertou {ambas_certas} notas completamente!\n"
                f"- Afinação: {round(afinacao_porcentagem * 100, 2)}%\n"
                f"- Duração: {round(duracao_porcentagem * 100, 2)}%\n"
                f"- Pontuação total: {score} {emoji}")

    print(feedback)
    
    return feedback
