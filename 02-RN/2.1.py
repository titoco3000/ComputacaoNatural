import bmp_reader
from perceptron_multiplas_saidas import Perceptron
import funcoes_de_ativacao as func

entradas = bmp_reader.read()
saidas = [
    [1 if j == i else 0 for j in range(len(entradas))] for i in range(len(entradas))
]

funcoes_de_ativacao = [func.sigmoid, func.relu, func.degrau]
taxas_de_aprendizagem = [0.5, 0.1, 0.01]

resultados = []
for func in funcoes_de_ativacao:
    for taxa in taxas_de_aprendizagem:
        p = Perceptron(len(entradas[0]), len(saidas[0]))
        rodadas_de_treino = p.treinar(entradas, saidas, erro_objetivo=0.01)
        print(f"Chegou em erro {p.erro_quad_medio} em {rodadas_de_treino} epochs")
        print(
            f"com função de ativação {func.__name__} e taxa de aprendizagem de {int(taxa*100)}%\n"
        )
        resultados.append((rodadas_de_treino, p, func, taxa))

# Escolhe o com treino mais rapido
_, melhor_modelo, func, taxa = min(resultados, key=lambda x: x[0])

print(
    f"O melhor modelo é o com função de ativação {func.__name__} e taxa de aprendizagem de {int(taxa*100)}%\n"
)
