import pandas as pd
from leilao import Leilao, Leiloes

if __name__ == '__main__':
    df_leiloes = pd.read_csv('cadastro.csv', sep=';')
    leiloes_list = [Leilao(**args) for args in df_leiloes.to_dict(orient="records")]
    leiloes = Leiloes(leiloes_list)

    for leilao in leiloes:
        print(leilao.site)