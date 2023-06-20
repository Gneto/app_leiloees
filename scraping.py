import pandas as pd
from bs4 import BeautifulSoup
import requests
import shutil
import time

from config import UPLOAD_PATH


class Scraping:
    def __init__(self, site, parameters):
        self.site = site
        self.parameters = parameters

        self.page = requests.get(site).content
        self.soup = BeautifulSoup(self.page, 'html.parser')

    def busca_texto(self, url, chave) -> pd.DataFrame:
        page = requests.get(url+chave).content
        soup = BeautifulSoup(page, 'html.parser')

        itens = []
        for lote in soup.select('.lote'):
            item = lote.select_one('.lote-content')
            lote_id = ''.join(filter(lambda i: i if i.isdigit() else None, lote.attrs['id']))

            self.busca_imagens_lote(lote_id) # busca as imagens por lote

            itens.append({
                    'lote': lote_id,
                    'titulo': item.select_one('div > a > h3').text,
                    'descricao': item.select_one('div > p.descricao').text,
                    'praca': item.select_one('.info-more > .right-infos > p').text,
                    'lances': item.select_one('.lote-stats > .lances > span').text,
                    'lance_inicial': item.select_one('.lote-stats > .valorAtual > span').text
            })
            
        return pd.DataFrame(itens)
    
    def busca_imagens_lote(self, lote):

        page = requests.get(f'http://saraivaleiloes.com.br/lote/{lote}/lote').content
        soup = BeautifulSoup(page, 'html.parser')

        for box in soup.select('.box-left'):
            imagem = box.select_one('.lote-thumbs > li > a > img')
            r = requests.get(imagem.attrs['src'], stream=True)

            if r.status_code == 200:
                timestamp = time.time()
                with open(f'{UPLOAD_PATH}/lote-{lote}-{timestamp}.jpg', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

if __name__ == '__main__':
    '''
    https://www.superbid.net/busca/compressor?searchType=opened&pageNumber=1&pageSize=30
    http://saraivaleiloes.com.br/busca?busca=compressor
    https://www.vipleiloes.com.br/Veiculos/ListarVeiculos?PalavraChave=compressor

    '''

    chave = 'compressor'
    url = f'https://www.superbid.net/busca/{chave}'
    scrap = Scraping(url, chave)

    print(scrap.soup)

    # itens = []
    # for box in scrap.soup.select('.MuiGrid-item'):
    #     item = box.select_one('div > div')
    #     print(box)

    

    # lotes_df = scrap.busca_texto(url, chave)
    # print(lotes_df)


    # Scraping('https://saraivaleiloes.com.br/busca')
    