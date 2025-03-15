from matrix import Matrix
import math


def _sigmoid(x):
    return 1 / (1 + math.e ** (-x))


def _sigmoid_deriv(x):
    return _sigmoid(x) * (1 - _sigmoid(x))


if __name__ == "__main__":

    peso_camada_oculta = Matrix([[0.1, 0.1], [0.1, 0.1], [0.1, 0.1]])
    peso_camada_saida = Matrix([[0.1, 0.1], [0.1, 0.1], [0.1, 0.1]])

    # 2 entradas + bias
    entrada = Matrix([1, 1, 1])
    saida_esperada = Matrix([1, 1])

    saida_camada_oculta = (entrada * peso_camada_oculta).aplicar_a_todos(_sigmoid)
    print(saida_camada_oculta)
    # ┌                                       ┐
    # │ 0.574442516811659 0.574442516811659 1 │
    # └                                       ┘

    # Adiciona o valor 1 para o bias
    entrada_camada_final = Matrix([l + [1] for l in saida_camada_oculta.val])

    saida_camada_final = (entrada_camada_final * peso_camada_saida).aplicar_a_todos(
        _sigmoid
    )

    print(saida_camada_final)
    # ┌                                       ┐
    # │ 0.5535163484824662 0.5535163484824662 │
    # └                                       ┘

    erro = saida_esperada - saida_camada_final

    print(erro)
# ┌                                       ┐
# │ 0.4464836515175338 0.4464836515175338 │
# └                                       ┘

gradiente_saida = erro * saida_camada_final.aplicar_a_todos(_sigmoid_deriv)

print(gradiente_saida)
