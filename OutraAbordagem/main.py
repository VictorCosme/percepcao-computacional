# from processador_partitura import *
from processador_audio import *
from comparador import *
from pontuador import *

nome_arquivo_json = "bella_prova"
previstas = processar_partitura(nome_arquivo_json)
print(previstas)
print(len(previstas))
print()

caminho_audio = f"{nome_arquivo_json}.wav"
detectadas = processar_audio(caminho_audio, previstas)
print(detectadas)
print(len(detectadas))
print()

avaliacao = avaliar_execucao(previstas, detectadas)
print(gerar_feedback(avaliacao))
