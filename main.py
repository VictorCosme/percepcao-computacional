def main(partitura, delay, naipe):
    melodia, notas_esperadas, num_divisoes = gerar_midi(partitura)

    canto = executar_e_gravar(melodia, delay)
    canto = tratar_audio(canto, naipe)

    notas_cantadas = get_notas_cantadas(canto, num_divisoes)
    
    return avaliar_canto(notas_cantadas, notas_esperadas)


def gerar_midi(partitura):
    pass


def executar_e_gravar(melodia, delay):
    """executa paralelamente os métodos executar_melodia() e
    capturar_audio()"""
    #executar(melodia, delay)
    #canto = capturar_audio()
    return canto
    

def executar(melodia, delay):
    pass


def capturar_audio():
    pass


def tratar_audio(audio, naipe):
    """corta e filtra o audio de acordo com as frequencias do naipe vocal"""
    pass


def get_notas_cantadas(audio, num_divisoes):
    notas_cantadas = [
        get_nota(audio_slice) 
        for audio_slice in slice(audio, num_divisoes)
    ]
    return notas_cantadas


def slice(audio, num_divisoes):
    pass


def get_nota(audio_slice):
    pass


def avaliar_canto(notas_cantadas, notas_esperadas):
    score = 0
    #todo
    return score 




if __name__ == '__main__':
    partitura = None
    delay = None
    naipe = None

    res = main(partitura, delay, naipe)
    print(res)
