'''
Problema do braço robótico
'''

import random
from algoritmo_genetico import algoritmo_genetico, plot

origem = (0,0)
deposito = (0,6)

caixas = [(3,4),(1,3),(2,5),(1,2),(5,1),(4,2)]

genoma = [1,2,4,5,1,4]

def corrigir_rota(rota):
    faltam = []
    desnecessarios = []
    for i in range(len(caixas)):
        achados = []
        for j in range(len(rota)):
            if rota[j] == i:
                achados.append(j)
        if len(achados) == 0:
            faltam.append(i)
        elif len(achados)>1:
            desnecessarios+=achados[1:]
    
    for f in faltam:
        rota[desnecessarios[0]] = f
        del desnecessarios[0]

def parada_aleatoria():
    return random.randint(0, len(caixas)-1)
    
def tamanho_da_rota(rota):
    carga = 0
    pos_atual = origem
    distancia = 0
    
    for i in rota:
        parada = caixas[i]
        distancia+=abs(pos_atual[0]-parada[0])+abs(pos_atual[1]-parada[1])
        pos_atual = parada
        carga+=1
        if carga==3:
            distancia+=abs(pos_atual[0]-deposito[0])+abs(pos_atual[1]-deposito[1])
            pos_atual = deposito
            carga=0
    
    return distancia

populacoes = [10, 100]
mut_rate = [0.1,0.01]
geracoes = [500, 1000]

resultados_gerais = []

# Para reprodutibilidade
random.seed(42)

for p in populacoes:
    for r in mut_rate:
        for g in geracoes:
            resultado = algoritmo_genetico(parada_aleatoria, tamanho_da_rota,len(caixas), func_correcao=corrigir_rota, pop=p, mut_rate=r, geracoes=g, minimizar=True)
            resultados_gerais.append(resultado)

melhor = min(resultados_gerais, key=lambda item: item["pontuacao"])

print(f"Rota: {','.join([f'P{i+1}' for i in melhor['melhor']])}; distancia: {melhor['pontuacao']}")

plot(resultados_gerais)
