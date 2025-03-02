'''
Problema da coloração de vértices no grafo, para minimizar as colisões de cores
'''

import random
from algoritmo_genetico import algoritmo_genetico, plot

grafo = {
    1: {5:1, 6:1, 8:1, 9:1},
    2: {4:1,7:1,6:1,10:1},
    3: {5:1,6:1,10:1,8:1},
    4: {2:1,7:1,9:1},
    5: {1:1,9:1,8:1,10:1,3:1},
    6: {2:1,10:1,3:1,1:1,9:1},
    7: {4:1,8:1,2:1},
    8: {7:1,1:1,5:1,3:1},
    9: {4:1,1:1,5:1,6:1},
    10: {2:1,6:1,5:1,3:1}
}

# maior é melhor
def encontros_cores(cores):
    r = len(cores)**2
    for node in grafo:
        for aresta in grafo[node]:
            if cores[node-1] == cores[aresta-1]:
                r-=1
    return r

def cor_aleatoria():
    return random.choice(["vermelho", "azul", "amarelo", "verde"])

populacoes = [10, 100]
mut_rate = [0.01,0.00005]
geracoes = [500, 1000]

resultados_gerais = []

# Para reprodutibilidade
random.seed(42)

for p in populacoes:
    for r in mut_rate:
        for g in geracoes:
            resultado = algoritmo_genetico(cor_aleatoria,encontros_cores,len(grafo),pop=p, mut_rate=r, geracoes=g)
            resultados_gerais.append(resultado)

melhor = max(resultados_gerais, key=lambda item: item["pontuacao"])["melhor"]
for node in grafo:
    print(f"{node}: {melhor[node-1]}")

plot(resultados_gerais)
