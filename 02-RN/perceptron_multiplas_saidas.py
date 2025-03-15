from matrix import Matrix
import math
import random
from funcoes_de_ativacao import sigmoid


class Perceptron:
    def __init__(
        self,
        entradas,
        saidas,
        coef_aprendizagem=0.1,
        epochs=200,
        func_ativacao=sigmoid,
    ):
        self.pesos = Matrix(
            [
                [random.uniform(-0.5, 0.5) for i in range(saidas)]
                for j in range(entradas + 1)
            ]
        )
        self.coef_aprendizagem = coef_aprendizagem
        self.epochs = epochs
        self.erro_quad_medio = None
        self.func_ativacao = func_ativacao

    def _avaliar_entrada_com_bias(self, entrada):
        return (entrada * self.pesos).aplicar_a_todos(self.func_ativacao)

    def treinar(self, entradas, saidas, erro_objetivo=0):
        # Adiciona 1 a cada entrada, para o bias
        entradas = [Matrix(e + [1]) for e in entradas]
        # converte saidas para matrizes
        saidas = [Matrix(e) for e in saidas]

        j = 0
        while j < self.epochs and (
            self.erro_quad_medio is None or self.erro_quad_medio > erro_objetivo
        ):
            erro_quad = 0
            for i in range(len(entradas)):
                # print("entrada")
                # print(entradas[i])
                # print("pesos")
                # print(self.pesos)
                saida_obtida = self._avaliar_entrada_com_bias(entradas[i])
                erro = (saida_obtida - saidas[i]).transposta()
                # print("erro")
                # print(erro)
                erro_quad += erro.grand_sum() ** 2
                correcao = self.coef_aprendizagem * (erro * entradas[i]).transposta()
                # print("Correção")
                # print(correcao)
                self.pesos = self.pesos - correcao
            self.erro_quad_medio = erro_quad / len(entradas)
            j += 1
        return j

    def avaliar(self, entrada):
        return self._avaliar_entrada_com_bias(Matrix(entrada + [1]))


if __name__ == "__main__":
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

    p = Perceptron(2, 2, epochs=10000)

    rodadas_de_treino = p.treinar(entradas, saidas)

    print(f"Chegou em erro {p.erro_quad_medio} em {rodadas_de_treino} epochs")

    # print(p.avaliar([0, 1]))

    # # entradas e saidas defininindo uma triple-AND
    # entradas = [
    #     [1, 1, 1],
    #     [1, 1, 0],
    #     [1, 0, 1],
    #     [0, 1, 1],
    #     [0, 0, 1],
    #     [0, 1, 0],
    #     [1, 0, 0],
    #     [0, 0, 0],
    # ]
    # saidas = [[1], [0], [0], [0], [0], [0], [0], [0]]

    # p = Perceptron(3, 1)

    # rodadas_de_treino = p.treinar(entradas, saidas)

    # print(f"Chegou em erro {p.erro_quad_medio} em {rodadas_de_treino} epochs")

    # print(p.avaliar([1, 1, 1]))
