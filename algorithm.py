from datetime import date, timedelta

def calcula_proxima_revisao(qualidade, repeticoes, intervalo, ft_facil):
    if qualidade < 3:
        intervalo = 1
        repeticoes = 0
    else:
        if repeticoes == 0:
            intervalo = 1
        elif repeticoes == 1:
            intervalo = 6
        else:
            intervalo *= ft_facil
        repeticoes+= 1

    ft_facil = ft_facil + (0.1 - (5 - qualidade) * (0.08 + (5 - qualidade) * 0.02))
    ft_facil = max(1.3, round(ft_facil, 2))

    prox_data = date.today() + timedelta(days = intervalo)
    
    return intervalo, repeticoes, ft_facil, prox_data
    
def ajustar_qualidade_tempo(qualidade, tmp_sec):
    if qualidade >= 3:
        if tmp_sec > 20:
            qualidade -= 2
        elif tmp_sec > 10:
            qualidade -= 1
    if qualidade < 3:
        qualidade = 3
    
    return qualidade
