class Linha:
    def __init__(self, tag, conjunto, dados) -> None:
        self.tag = tag
        self.conjunto = conjunto
        self.dados = dados

class Cache:
    def __init__(self, n_conjuntos, linhas_por_conjunto):
        self.n_conjuntos = n_conjuntos
        self.linhas_por_conjunto = linhas_por_conjunto
        self.bytes_por_linha = 8
        
        conjuntos = {}
        for i in range(n_conjuntos):
            conjuntos[i] = []
        self.cache = conjuntos
