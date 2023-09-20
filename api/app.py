from flask import Flask, render_template
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from models import getSelecoesData

app = Flask(__name__, template_folder='')

# Lista de seleções mundiais para os dois grupos
grupo1 = ["Brasil", "Alemanha", "Argentina", "Itália"]
grupo2 = ["França", "Espanha", "Inglaterra", "Holanda"]

# Probabilidades de vitória de cada seleção em relação a outra
# Os valores variam de 0 a 1, onde 0 significa nenhuma chance de vitória e 1 significa certeza de vitória.
probabilidades_grupo1 = np.array([
    [0.5, 0.4, 0.6, 0.7],  # Brasil
    [0.6, 0.5, 0.4, 0.5],  # Alemanha
    [0.4, 0.6, 0.5, 0.3],  # Argentina
    [0.3, 0.5, 0.7, 0.5]   # Itália
])

probabilidades_grupo2 = np.array([
    [0.5, 0.4, 0.6, 0.7],  # França
    [0.6, 0.5, 0.4, 0.5],  # Espanha
    [0.4, 0.6, 0.5, 0.3],  # Inglaterra
    [0.3, 0.5, 0.7, 0.5]   # Holanda
])

# Função para gerar resultados de partidas com base nas probabilidades
def gerar_resultados(probabilidades):
    resultados = []
    adversarios = []
    for i in range(len(probabilidades)):
        partida = []
        adversario_partida = []
        for j in range(len(probabilidades[i])):
            # Garante que não haverá partidas entre o mesmo time
            if i == j:
                partida.append("Não ocorreu")
            else:
                # Gere um número aleatório entre 0 e 1
                resultado = random.random()
                # Verifique se a seleção i ganhou a partida com base na probabilidade
                if resultado <= probabilidades[i][j]:
                    partida.append("Vitória")
                else:
                    partida.append("Derrota")
                adversario_partida.append(grupo1[j] if i < len(grupo1) else grupo2[j])
        resultados.append(partida)
        adversarios.append(adversario_partida)
    return resultados, adversarios

# Gere os resultados das partidas e os adversários para ambos os grupos
resultados_grupo1, adversarios_grupo1 = gerar_resultados(probabilidades_grupo1)
resultados_grupo2, adversarios_grupo2 = gerar_resultados(probabilidades_grupo2)


# Função para calcular a pontuação de cada seleção
def calcular_pontuacao(resultados):
    pontuacao = [0] * len(resultados)
    for i in range(len(resultados)):
        for j in range(len(resultados[i])):
            if resultados[i][j] == "Vitória":
                pontuacao[i] += 3
            elif resultados[i][j] == "Empate":
                pontuacao[i] += 1
    return pontuacao

# Calcula a pontuação de cada grupo
pontuacao_grupo1 = calcular_pontuacao(resultados_grupo1)
pontuacao_grupo2 = calcular_pontuacao(resultados_grupo2)

# Classifica as seleções por pontuação
classificacao_grupo1 = [x for _, x in sorted(zip(pontuacao_grupo1, grupo1), reverse=True)]
classificacao_grupo2 = [x for _, x in sorted(zip(pontuacao_grupo2, grupo2), reverse=True)]

# Define os finalistas de cada grupo
finalistas_grupo1 = classificacao_grupo1[:2]
finalistas_grupo2 = classificacao_grupo2[:2]

# Função para realizar a final entre os dois finalistas
def final(finalistas, probabilidades):
    final_resultados, final_adversarios = gerar_resultados(probabilidades)
    final_pontuacao = calcular_pontuacao(final_resultados)
    vencedor = finalistas[0] if final_pontuacao[0] > final_pontuacao[1] else finalistas[1]
    return vencedor

# Realiza a final entre os finalistas de cada grupo
campeao_grupo1 = final(finalistas_grupo1, probabilidades_grupo1)
campeao_grupo2 = final(finalistas_grupo2, probabilidades_grupo2)

# Crie um grafo para visualizar os resultados das partidas
def criar_grafo(resultados, selecoes, adversarios):
    G = nx.Graph()
    for i, selecao in enumerate(selecoes):
        G.add_node(selecao)
        for j, adversario in enumerate(adversarios[i]):
            if resultados[i][j] == "Não ocorreu":
                continue
            if resultados[i][j] == "Vitória":
                G.add_edge(selecao, adversario)
    return G

grafo_grupo1 = criar_grafo(resultados_grupo1, grupo1, adversarios_grupo1)
grafo_grupo2 = criar_grafo(resultados_grupo2, grupo2, adversarios_grupo2)

# Função para salvar o gráfico em um arquivo de imagem
def salvar_grafico_em_imagem(grafo):
    pos = nx.spring_layout(grafo)
    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, font_weight='bold', node_size=500, node_color='lightblue')
    img_io = BytesIO()
    plt.savefig(img_io, format='PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

@app.route("/")
def show_results():
    img_data_grupo1 = salvar_grafico_em_imagem(grafo_grupo1)
    img_data_grupo2 = salvar_grafico_em_imagem(grafo_grupo2)

    # Cálculo do campeão geral
    campeao_final = campeao_grupo1 if pontuacao_grupo1[0] > pontuacao_grupo2[0] else campeao_grupo2
    print(getSelecoesData())
    return render_template('resultados.html',
                           grupo1=grupo1, grupo2=grupo2,
                           resultados_grupo1=resultados_grupo1,
                           resultados_grupo2=resultados_grupo2,
                           adversarios_grupo1=adversarios_grupo1,
                           adversarios_grupo2=adversarios_grupo2,
                           pontuacao_grupo1=pontuacao_grupo1,
                           pontuacao_grupo2=pontuacao_grupo2,
                           classificacao_grupo1=classificacao_grupo1,
                           classificacao_grupo2=classificacao_grupo2,
                           finalistas_grupo1=finalistas_grupo1,
                           finalistas_grupo2=finalistas_grupo2,
                           campeao_grupo1=campeao_grupo1,
                           campeao_grupo2=campeao_grupo2,
                           campeao_final=campeao_final,
                           img_data_grupo1=img_data_grupo1,
                           img_data_grupo2=img_data_grupo2)

if __name__ == '__main__':
    app.run(debug=True)