"""
Módulo responsável por:
Aplicar pré-processamento no .wav (filtros, remoção de ruído)
Cortar o áudio em segmentos conforme a partitura
"""

import librosa
import numpy as np
import sounddevice as sd


def limpar_audio(audio: np.ndarray, sr: int, duracao_minima: float) -> tuple[np.ndarray, int]:
    """
    Limpa os silêncios iniciais e finais de um trecho de áudio.
    """
    audio_limpo, _ = librosa.effects.trim(audio, top_db=30)

    duracao_atual = len(audio_limpo) / sr
    if duracao_atual < duracao_minima:
        falta = int((duracao_minima - duracao_atual) * sr)
        audio_limpo = np.concatenate([audio_limpo, np.zeros(falta)])

    return audio_limpo, sr


def segmentar_audio(audio: np.ndarray, sr: int, notas: list[dict]) -> list[tuple[str, np.ndarray]]:
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


def extrair_frequencia(segmento: np.ndarray, sr: int, naipe: str = "default") -> dict[str, str | float]:
    """
    Extrai a nota dominante de um segmento de áudio.
    Retorna a nota (ex. 'Fa#4') ou "rest" se nada for detectado.
    """
    duracao_segmento = len(segmento) / sr
    silencio = {"nota": "rest", "duracao": duracao_segmento}

    energia = np.mean(np.abs(segmento))
    limiar = 0.001
    if energia < limiar:
        return silencio

    naipes = {
        "default": {"fmin": librosa.note_to_hz("C2"), "fmax": librosa.note_to_hz("C7")},
        "baixo": {"fmin": librosa.note_to_hz("E2"), "fmax": librosa.note_to_hz("G4")},
        "baritono": {"fmin": librosa.note_to_hz("A2"), "fmax": librosa.note_to_hz("A4")},
        "tenor": {"fmin": librosa.note_to_hz("C3"), "fmax": librosa.note_to_hz("C5")},
        "contralto": {"fmin": librosa.note_to_hz("C3"), "fmax": librosa.note_to_hz("G5")},
        "soprano": {"fmin": librosa.note_to_hz("C4"), "fmax": librosa.note_to_hz("C6")},
        "mezzo-soprano": {"fmin": librosa.note_to_hz("A3"), "fmax": librosa.note_to_hz("A5")}
    }
    naipe = naipes.get(naipe, naipes["default"])
    fmin = naipe["fmin"]
    fmax = naipe["fmax"]

    hop_length = 512
    f0, voiced_flag, voiced_probs = librosa.pyin(
        segmento,
        fmin=fmin,
        fmax=fmax,
        sr=sr,
        hop_length=hop_length
    )

    f0_valido = f0[voiced_flag]
    if f0_valido is None or len(f0_valido) == 0:
        return silencio

    mediana = np.median(f0_valido)
    nota_detectada = freq_para_nota(mediana)

    if nota_detectada is None:
        return silencio

    duracao_detectada = len(f0_valido) * hop_length / sr

    return {"nota": nota_detectada, "duracao": round(duracao_detectada, 3)}


def extrair_notas_segmentos(segmentos: list[tuple[str, np.ndarray]], sr: int, naipe: str = "default") \
        -> tuple[list[dict[str, str | float]], float]:
    notas_detectadas = []
    for nova_prevista, segmento in segmentos:
        resultado = extrair_frequencia(segmento, sr, naipe)
        notas_detectadas.append(resultado)

    duracao = 0
    for nota in notas_detectadas:
        duracao += nota["duracao"]

    return notas_detectadas, round(duracao, 3)


def processar_audio(arquivo_wav: str, previstas: list[dict], duracao_minima: float, naipe: str = "default") -> tuple[list[dict[str, str | float]], float]:
    if not arquivo_wav.endswith(".wav"):
        arquivo_wav += ".wav"

    audio, sr = librosa.load(arquivo_wav, sr=None)
    audio_filtrado, sr = limpar_audio(audio, sr, duracao_minima)
    sd.play(audio_filtrado, sr)
    sd.wait()

    segmentos = segmentar_audio(audio_filtrado, sr, previstas)

    return extrair_notas_segmentos(segmentos, sr, naipe)
