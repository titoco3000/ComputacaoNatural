from matrix import Matrix

# entradas e saidas defininindo uma soma binaria
entradas = [
    [1, 1],
    [0, 1],
    [1, 0],
    [0, 0],
]
saidas = [
    [1, 1],
    [0, 1],
    [0, 1],
    [0, 0],
]


# para cada entrada, adiciona a entrada para o bias (sempre 1)
for e in entradas:
    e.append(1)
# converte para matrizes
entradas = [Matrix(e) for e in entradas]
saidas = [Matrix(e) for e in saidas]

# (1 peso para cada entrada + bias) para cada saida
pesos = Matrix(
    [
        [0, 0, 0],
        [0, 0, 0],
    ]
).transposta()

coef_aprendizagem = 0.1
epochs = 200
erro_quad_medio = 1
j = 0
while j < epochs and erro_quad_medio > 0:
    erro_quad = 0
    for i in range(len(entradas)):
        print(f"i = {i}")
        print("in:")
        print(entradas[i])
        print("w:")
        print(pesos)
        print("multiplicados:")
        print(entradas[i] * pesos)
        saida_obtida = (entradas[i] * pesos).aplicar_a_todos(
            lambda x: 1 if x > 1 else 0
        )
        print("out:")
        print(saida_obtida)
        erro = (saida_obtida - saidas[i]).transposta()
        print("erro:")
        print(erro)
        erro_quad += erro.grand_sum() ** 2
        correcao = coef_aprendizagem * (erro * entradas[0]).transposta()
        print("correcao")
        print(correcao)
        pesos = pesos - correcao
    erro_quad_medio = erro_quad / len(entradas)
    print(pesos, erro_quad_medio)
    j += 1

print(f"Chegou em erro {erro_quad_medio} em {j} epochs")
