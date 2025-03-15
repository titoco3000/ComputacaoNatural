import bmp_reader
from perceptron_multiplas_saidas import Perceptron
import funcoes_de_ativacao as func
import random

entradas = bmp_reader.read()
saidas = [
    [1 if j == i else 0 for j in range(len(entradas))] for i in range(len(entradas))
]

funcoes_de_ativacao = [func.sigmoid, func.relu, func.degrau]
taxas_de_aprendizagem = [0.5, 0.1, 0.01]

for ruido in [0.05, 0.1, 0.15, 0.2]:
    print(f"ruido: {ruido*100}%")
    entradas_alteradas = [
        [num if random.random() > ruido else (num + 1) % 2 for num in entrada]
        for entrada in entradas
    ]
    resultados = []
    for func in funcoes_de_ativacao:
        for taxa in taxas_de_aprendizagem:
            p = Perceptron(len(entradas[0]), len(saidas[0]))
            rodadas_de_treino = p.treinar(entradas, saidas, erro_objetivo=0.01)
            print(
                f"Função de ativação {func.__name__} e taxa de aprendizagem de {int(taxa*100)}%"
            )
            print(
                f"obteve erro de treinamento de {p.erro_quad_medio} em {rodadas_de_treino} epochs."
            )
            resultados.append((rodadas_de_treino, p, func, taxa))

            acertos = 0
            for i in range(len(entradas_alteradas)):
                r = p.avaliar(entradas_alteradas[i]).val[0]
                index_max_obtido = max(range(len(r)), key=r.__getitem__)
                index_max_correto = max(
                    range(len(saidas[i])), key=saidas[i].__getitem__
                )
                if index_max_obtido == index_max_correto:
                    acertos += 1
            print(
                f"Dos {len(entradas_alteradas)} numeros modificados, acertou {acertos}"
            )

    # Escolhe o com treino mais rapido
    _, melhor_modelo, func, taxa = min(resultados, key=lambda x: x[0])

    print(
        f"O melhor modelo é o com função de ativação {func.__name__} e taxa de aprendizagem de {int(taxa*100)}%\n"
    )
