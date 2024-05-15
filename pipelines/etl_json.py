# ETL de arquivos JSON
# Desenvolvimento da ETL de forma simples extraindo e transformando dados utilizando a biblioteca Pandas do python

import pandas as pd
from pandas import DataFrame
import re
from typing import List, Dict, Any

def leitor_json(arquivo: str) -> DataFrame:
    dados = pd.read_json(arquivo)
    return dados

def converte_medidas(dados: str) -> DataFrame:
    pattern: str = re.compile(r'\d+(\.\d+)?')
    pesos_kg: list = []
    larguras_metros: list = []
    comprimentos_metros: list = []

    for peso in dados['Peso']:
        match: float = pattern.search(peso)
        if match:
            valor_numerico: float = float(match.group())
            valor_kg: float = valor_numerico * 0.453592  # Convertendo libras para quilogramas
            pesos_kg.append(f'{valor_kg:.2f}')            
            
    for largura in dados['Largura']:
        match_1: float = pattern.search(largura)
        if match:
            valor_numerico_largura: float = float(match_1.group())
            valor_larg_metros: float = valor_numerico_largura * 0.3048  # Convertendo pés para metros
            larguras_metros.append(f'{valor_larg_metros:.2f}')
    
    for comprimento in dados['Comprimento']:
        match_2: float = pattern.search(comprimento)
        if match:
            valor_numerico_comprimento: float = float(match_2.group())
            valor_metros: float = valor_numerico_comprimento * 0.3048  # Convertendo pés para metros
            comprimentos_metros.append(f'{valor_metros:.2f}')
    
    dados['Peso Kg'] = pesos_kg 
    dados['Largura M2'] = larguras_metros
    dados['Comprimento M2'] = comprimentos_metros
    
    return dados


def main():
    nome_arquivo = './data/produtos.json'
    dados_brutos = leitor_json(nome_arquivo)
    dados_processados = converte_medidas(dados_brutos)
    df_json_pronto = dados_processados.drop(['Peso', 'Largura', 'Comprimento'], axis=1)
    return df_json_pronto
if __name__ == '__main__':
    main()


