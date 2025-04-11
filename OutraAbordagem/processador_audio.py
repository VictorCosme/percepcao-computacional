"""
Módulo responsável por:
Aplicar pré-processamento no .wav (filtros, remoção de ruído)
Cortar o áudio em segmentos conforme a partitura
"""

import librosa
import numpy as np


def limpar_audio(audio):
    # TODO
    pass


def segmentar_audio(audio, sr, notas):
    """
    Segmenta o áudio conforme os tempos das notas esperadas.
    Retorna uma lista de tuplas (nota_esperada, trecho_do_audio)
    """
    segmentos = []

    for evento in notas:
        nota = evento["nota"]
        inicio = evento["inicio"]
        duracao = evento["duracao"]

        inicio_sample = int(inicio * sr)
        final_sample = int((inicio + duracao) * sr)
        segmento = audio[inicio_sample:final_sample]

        segmentos.append((nota, segmento))

    return segmentos


def freq_para_nota(freq: float) -> str | None:
    """
    Recebe uma frequência e retorna a nota associada.
    """
    if freq is None or freq <= 0:
        return None

    notas = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    semitons = round(12 * np.log2(freq / 440.0))
    nota = notas[(semitons + 9) % 12]
    oitava = 4 + ((semitons + 9) // 12)

    return f"{nota}{oitava}"


def extrair_frequencia(segmento, sr):
    """
    Extrai a nota dominante de um segmento de áudio.
    Retorna a nota (ex. 'Fa#4') ou None se nada for detectado.
    """
    energia = np.mean(np.abs(segmento))
    limiar = 0.001

    duracao_segmento = len(segmento) / sr
    silencio = {"nota": "rest", "duracao": duracao_segmento}

    if energia < limiar:
        return silencio

    hop_length = 512
    f0, voiced_flag, voiced_probs = librosa.pyin(
        segmento,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr,
        hop_length=hop_length
    )

    f0_valido = f0[voiced_flag]
    mediana = np.median(f0_valido) if len(f0_valido) > 0 else None
    nota_detectada = freq_para_nota(mediana)

    if nota_detectada is None:
        return silencio

    duracao_detectada = len(f0_valido) * hop_length / sr

    return {"nota": nota_detectada, "duracao": duracao_detectada}


def processar_audio(caminho_audio, notas_previstas):
    audio, sr = librosa.load(caminho_audio, sr=None)

    segmentos = segmentar_audio(audio, sr, notas_previstas)

    notas_detectadas = []
    for nova_prevista, segmento in segmentos:
        resultado = extrair_frequencia(segmento, sr)
        notas_detectadas.append(resultado)

    return notas_detectadas
