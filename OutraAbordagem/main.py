from processador_partitura import *
from processador_audio import *
from comparador import *
from pontuador import *

# notas = ["Do#4", "Do4", "Fa#4"]
# for n in notas:
# nome_arquivo_json = f"wavs_controlados/{n}"

musica = f"bella_prova"
print(f"Processando a partitura para a melodia {musica}...")
previstas = processar_partitura(musica)
print(f"Partitura processada com sucesso. Foram encontradas {len(previstas[0])} notas.")
print(f"Duração necessária aproximada de {previstas[1]} seg.")
print()

print(f"Processando e executando o áudio da música {musica}...")
detectadas = processar_audio(musica, previstas[0], previstas[1])
print(f"Áudio processado com sucesso. Foram encontradas {len(detectadas[0])} notas.")
print(f"Duração obtida aproximada de {detectadas[1]} seg.")
print()

print(f"Comparando e gerando o feedback...")
tolerancia_afinacao = 2
tolerancia_duracao = 0.25
peso_afinacao = 0.6
avaliacao = avaliar_execucao(previstas[0], detectadas[0], tolerancia_afinacao, tolerancia_duracao)
print(gerar_feedback(avaliacao, peso_afinacao))
print()
