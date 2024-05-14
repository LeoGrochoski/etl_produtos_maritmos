# ETL de arquivos CSV
# Desenvolvimento da ETL de forma simples extraindo e transformando dados utilizando o modulo nativo CSV do python

import csv
import re
import pandas as pd
from typing import List, Dict, Any

# Extração dos dados do arquivo CSV
def leitor_csv(arquivo: str) -> List[Dict[str, Any]]:
    """Funcao reliza a extracao dos dados no formato bruto do documento .csv

    Args:
        arquivo (str): arquivo em formato .csv para extracao dos dados

    Returns:
        List[Dict[str, Any]]: dado bruto extraido 
    """
    with open(arquivo, 'r') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        lista_dicionario = [row for row in leitor_csv]
    return lista_dicionario

# Processamento dos dados, transformação para float 

def processamento_dados(lista_dicionario: List[Dict[str, float]]) -> List[Dict[str, float]]:
    # regex para localizar os valores numericos
    padrao = re.compile(r'\d+(\.\d+)?')
    for dicionario in lista_dicionario:
        res_peso = padrao.search(dicionario['Peso (lbs)'])
        res_comprimento = padrao.search(dicionario['Comprimento (ft)'])
        res_largura = padrao.search(dicionario['Largura (ft)'])
        if res_peso:
            peso_num: float = float(res_peso.group())
            dicionario['Peso (lbs)'] = peso_num
        if res_comprimento:
            comprimento_num: float = float(res_comprimento.group())
            dicionario['Comprimento (ft)'] = comprimento_num
        if res_largura:
            largura_num: float = float(res_largura.group())
            dicionario['Largura (ft)'] = largura_num
    return lista_dicionario

# Conversão das metricas de medidas imperiais para SI

conversor_kg: float = 2.20462
conversor_metros: float = 0.3048


def conversor_medidas(lista_dicionario: List[Dict[str, float]]) -> List[Dict[str, float]]:
    for dicionario in lista_dicionario:
        peso_convertido: float = (dicionario['Peso (lbs)'] / conversor_kg)
        dicionario['Peso (lbs)']: float = float(f'{peso_convertido:.2f}') # type: ignore
        comprimento_convertido: float = (dicionario['Comprimento (ft)'] * conversor_metros)
        dicionario['Peso (lbs)'] = float(f'{comprimento_convertido:.2f}')
        largura_convertido: float = (dicionario['Largura (ft)'] * conversor_metros)
        dicionario['Largura (ft)'] = float(f'{largura_convertido:.2f}')
    return lista_dicionario

# Função principal

def main():
    nome_arquivo = './data/produtos.csv'
    dados_brutos = leitor_csv(nome_arquivo)
    dados_processados = processamento_dados(dados_brutos)
    dados_convertidos = conversor_medidas(dados_processados)
    df_produtos_kg = pd.DataFrame(dados_convertidos)
    df_csv_pronto = df_produtos_kg.rename(columns={"Peso (lbs)": "Peso Kg", "Largura (ft)": "Largura M2", "Comprimento (ft)": "Comprimento M2"})
    return df_csv_pronto

if __name__ == '__main__':
    main()

