import json

def getSelecoesData():
    urlJsonFile = 'selecoes.json'
    with open(urlJsonFile, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)