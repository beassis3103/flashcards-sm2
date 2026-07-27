"""
Significado de cada variável:
qualidade: nota dada pelo usuário de como foi responder a pergunta (0-2: errou; 3-5: acertou)
repeticoes: quantas vezes seguidas o usuário acertou esse cartão
intervalo: quantidade de dias até a aparição do próximo cartão
ft_facil: fator de facilidade desse cartão, começa em 2.5 e nunca fica abaixo de 1.3 (é um valor definido pela fórmula de Wozniak)
tmp_sec: tempo em segundos que o usuário demorou para responder a pergunta
"""

from datetime import date, timedelta

def calcula_proxima_revisao(qualidade, repeticoes, intervalo, ft_facil):
    #Se o intervalo < 3 quer dizer que o usuário errou a pergunta, então o cartão aparecerá no dia seguinte
    if qualidade < 3:
        intervalo = 1
        repeticoes = 0

    #Se for > 3 quer dizer que o usuário acertou a pergunta; 
    #Dependendo de quantas vezes seguidas o usuário acertou essa pergunta, o intervalo de aparições aumenta
    else
        if repeticoes == 0:
            intervalo = 1
        elif repeticoes == 1:
            intervalo = 6
        else:
            intervalo *= ft_facil
        repeticoes+= 1

    #Fórmula de Wozniak, que calcula se o cartão atual ficou mais fácil ou maisa difícil para o usuário de acordo com as vraiáveis acima
    ft_facil = ft_facil + (0.1 - (5 - qualidade) * (0.08 + (5 - qualidade) * 0.02))
    ft_facil = max(1.3, round(ft_facil, 2))

    #Calcula a próxima data de acordo com a nova variação do intervalo
    prox_data = date.today() + timedelta(days = intervalo)
    
    return intervalo, repeticoes, ft_facil, prox_data
    

#Ajusta a qualidade de acordo com o tempo em que o usuário demorou para responder a pergunta, caso tenha acertado
def ajustar_qualidade_tempo(qualidade, tmp_sec):
    #Verifica se o usuário acertou, caso não, a qualidade permanece a mesma
    if qualidade >= 3:
        #É feita uma dinâmica: dependendo do tempo em segundos que o usuário demorou para responder, é tirada certa pontuação da qualidade
        if tmp_sec > 20:
            qualidade -= 2
        elif tmp_sec > 10:
            qualidade -= 1
    #Depois da penalidade, caso a qualidade tenha ficado < 3, o valor é setado como = 3, sendo a menor pontuação da categoria "acertos"
    if qualidade < 3:
        qualidade = 3
    
    return qualidade
