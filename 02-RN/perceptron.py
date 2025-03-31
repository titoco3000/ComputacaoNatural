from matrix import Matrix
import math


def _sigmoid(x):
    return 1 / (1 + math.e ** (-x))


def _sigmoid_deriv(y):
    return y * (1 - y)


peso_camada_oculta = Matrix([[0.1, 0.1], [0.1, 0.1], [0.1, 0.1]])
peso_camada_saida = Matrix([[0.1, 0.1], [0.1, 0.1], [0.1, 0.1]])

# 2 entradas + bias
entrada = Matrix([1, 1, 1])
saida_esperada = Matrix([1, 1])

print(entrada * peso_camada_oculta)

saida_camada_oculta = (entrada * peso_camada_oculta).aplicar_a_todos(_sigmoid)
print(saida_camada_oculta)

# [[0.574442516811659 0.574442516811659 1]]

# Adiciona o valor 1 para o bias
entrada_camada_final = Matrix([l + [1] for l in saida_camada_oculta.val])

saida_camada_final = (entrada_camada_final * peso_camada_saida).aplicar_a_todos(
    _sigmoid
)

print("saida_camada_final")
print(saida_camada_final)

# [[0.5535163484824662 0.5535163484824662]]

erro = saida_esperada - saida_camada_final

print("erro")
print(erro)
# [[0.4464836515175338 0.4464836515175338]]

coef_aprendizado = 0.1

# não sei se essa parte está certa
delta_saida = erro.elementwise_mul(saida_camada_final.aplicar_a_todos(_sigmoid_deriv))

print("delta_saida")
print(delta_saida)
# [[0.10348965119065406 0.10348965119065406]]

print("peso_camada_saida")
print(peso_camada_saida)

ajuste_peso_saida = entrada_camada_final.transposta() * delta_saida * coef_aprendizado
print("ajuste_peso_saida")
print(ajuste_peso_saida)

peso_camada_saida = peso_camada_saida + ajuste_peso_saida
print("peso_camada_saida")
print(peso_camada_saida)

# delta_oculta = (delta_saida * peso_camada_saida.transposta()
# print("delta_oculta")
# print(delta_oculta)
