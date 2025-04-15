"""Arquivo de execução para teste controlado.

ENTRADAS: 
- Partitura: Bella Prova
- Canto: WAV gerado a partir do MIDI da partitura
- Naipe: default

SAIDA:
- Espera-se um score excelente
"""

import processador_partitura
import processador_audio
import comparador
import pontuador

partitura = "teste-controlado/bella_prova.json"

previstas = processador_partitura.processar_partitura(
    arquivo_json=partitura
)

# Áudio pré-gravado usado para teste controlado. Compare com main_gravador
canto = "teste-controlado/bella_prova.wav" 

detectadas = processador_audio.processar_audio(
    arquivo_wav=canto,
    previstas=previstas[0],
    duracao_minima=previstas[1],
    naipe="default"
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
