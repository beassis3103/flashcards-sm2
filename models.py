class Pasta:
    def __init__(self, nome, id = None, dt_criacao = None):
        self.id = id
        self.nome = nome
        self.dt_criacao = dt_criacao

class Flashcard:
    def __init__(self, id, pasta_id, pergunta, resposta, intervalo = 0, repeticoes = 0, ft_facil = 2.5, prox_rev = None, err_seg = 0):
        self.id = id
        self.pasta_id = pasta_id
        self.pergunta = pergunta
        self.resposta = resposta
        self.intervalo = intervalo
        self.repeticoes = repeticoes
        self.ft_facil = ft_facil 
        self.prox_rev = prox_rev
        self.err_seg = err_seg
