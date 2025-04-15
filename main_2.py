"""Arquivo de execução para teste pré-gravado.

ENTRADAS: 
- Partitura: Bella Prova
- Canto: WAV pré-gravado
- Naipe: barítono

SAIDA:
- Espera-se um score baixo
"""

import processador_partitura
import processador_audio
import comparador
import pontuador

partitura = "teste-voz/bella_prova.json"

previstas = processador_partitura.processar_partitura(
    arquivo_json=partitura
)

canto = "teste-voz/joao-2.wav"
#canto = "teste-voz/joao-4.wav" # mp3

detectadas = processador_audio.processar_audio(
    arquivo_wav=canto,
    previstas=previstas[0],
    duracao_minima=previstas[1],
    naipe="baritono"
)

avaliacao = comparador.avaliar_execucao(
    previstas = previstas[0],
    detectadas = detectadas[0],
    tolerancia_afinacao = 2,
    tolerancia_duracao = 0.25
)

# ---------------------------------------
# FRONT-END
# ---------------------------------------

pontuador.gerar_feedback(
    avaliacao,
    peso_afinacao = 0.6)
