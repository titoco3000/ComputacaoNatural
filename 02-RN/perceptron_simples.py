from matrix import Matrix

# entradas e saidas defininindo um triple-AND
entradas = [
    [1, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 0],
]
saidas = [1, 0, 0, 0, 0, 0, 0, 0]


# para cada entrada, adiciona a entrada para o bias (sempre 1)
for e in entradas:
    e.append(1)
# converte para matrizes
entradas = [Matrix(e) for e in entradas]

# 1 peso para cada entrada + bias
pesos = Matrix([0, 0, 0, 0]).transposta()


def perceptron(entrada, pesos):
    return 1 if (entrada * pesos).grand_sum() > 0 else 0


coef_aprendizagem = 0.1
epochs = 100
erro_quad_medio = 1
j = 0
while j < epochs and erro_quad_medio > 0:
    erro_quad = 0
    for i in range(len(entradas)):
        r = perceptron(entradas[i], pesos)
        erro = saidas[i] - r
        erro_quad += erro * erro
        r = erro * entradas[i]
        novos_pesos = pesos + coef_aprendizagem * r.transposta()
        pesos = novos_pesos
    erro_quad_medio = erro_quad / len(entradas)
    print(pesos, erro_quad_medio)
    j += 1

print(f"Chegou em erro {erro_quad_medio} em {j} epochs")
