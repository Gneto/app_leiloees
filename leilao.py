import pandas as pd


class Leilao:

    def __init__(self, nome, cnpj, endereco, site, telefone, email):
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.site = site
        self.telefone = telefone
        self.email = email

class Leiloes(list):
    def __init__(self, leiloes):
        super().__init__(leiloes)