"""
EC 4.2) Utilize o algoritmo CLONALG para obter uma classificação da base “Zoo”. Varie os
parâmetros de limiar de similaridade, tamanho da população e quantidade de iterações,
analisando o desempenho do algoritmo em cada cenário.
"""

import numpy as np
import random


def afinidade(antigeno, feature):
    return max(np.sum(feature == antigeno), 0.0001)


def mutar(elemento, taxa):
    return [(not n if random.random() < taxa else n) for n in elemento]


class Clonalg:
    def __init__(
        self,
        features,
        targets,
        classe,
        limiar_de_similaridade,
        tamanho_da_populacao,
        iteracoes,
        n1,
        n2,
        taxa_mutacao,
    ):
        self.m = []
        n_features = features.shape[1]

        antigenos = [
            feature
            for (index, feature), (index, target) in zip(
                features.iterrows(),
                targets.iterrows(),
            )
            if target.item() != classe.item()
        ]

        P = [np.random.randint(2, size=n_features) for _ in range(tamanho_da_populacao)]
        for i in range(iteracoes):
            for x in antigenos:
                afinidades = [(p, afinidade(x, p)) for p in P]
                afinidades.sort(key=lambda x: x[1])
                clones = [mutar(p[0], taxa_mutacao / p[1]) for p in afinidades[:n1]]
                P += clones

                afinidades = [(index, p, afinidade(x, p)) for index, p in enumerate(P)]
                afinidades.sort(key=lambda x: x[2])
                self.m.append(afinidades[0][0])
                for pior in afinidades[-n2:]:
                    del P[pior[0]]
                    # try:
                    #     self.m.remove(pior[0])
                    #     print("Removendo de m")
                    # except:
                    #     pass
                    P.append(np.random.randint(2, size=n_features))
            print(f"iteracao {i}")
            print(f"P: {len(P)}")
            print(f"m: {len(self.m)}")


if __name__ == "__main__":
    from ucimlrepo import fetch_ucirepo

    zoo = fetch_ucirepo(id=111)

    X = zoo.data.features
    y = zoo.data.targets

    classes = y.iloc[:, 0].unique()

    for classe in classes:
        print(classe)
        cl = Clonalg(X, y, classe, 1, 10, 10, 3, 50, 0.1)
