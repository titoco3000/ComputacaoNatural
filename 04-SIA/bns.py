import numpy as np  # type: ignore


class BNS:
    def __init__(
        self, features, targets, classe, max_tentativas, max_detectores, radius=1
    ):
        self.radius = radius
        self.detectores = []
        tentativa = 0
        n_features = features.shape[1]  # Número de colunas

        while len(self.detectores) < max_detectores and tentativa < max_tentativas:
            # Gera um detector aleatório de 0s e 1s do tamanho das features
            detector = np.random.randint(2, size=n_features)

            # Verifica a distância de Hamming em relação aos dados existentes
            valido = True
            for (index, feature), (index, target) in zip(
                features.iterrows(),
                targets.iterrows(),
            ):
                if target.item() == classe:
                    distancia = np.sum(
                        feature.values != detector
                    )  # Distância de Hamming
                    if distancia < radius:
                        valido = False
                        break

            # Se for válido, adiciona à lista de detectores
            if valido:
                self.detectores.append(detector)

            tentativa += 1

    # Retorna True se for reconhecido como self
    def monitorar(self, feature):
        for detector in self.detectores:
            distancia = np.sum(feature != detector)  # Distância de Hamming
            if distancia < self.radius:
                return False
        return True


class MultiBNS:
    def __init__(
        self,
        features,
        targets,
        max_tentativas_por_classe,
        max_detectores_por_classe,
        radius=1,
    ):
        self.classes = targets.iloc[:, 0].unique()
        self.classificadores = [
            BNS(
                features,
                targets,
                classe,
                max_tentativas_por_classe,
                max_detectores_por_classe,
                radius,
            )
            for classe in self.classes[:-1]
        ]

    def monitorar(self, feature):
        for classificador, classe in zip(self.classificadores, self.classes[:-1]):
            if classificador.monitorar(feature):
                return classe
        return self.classes[-1]


if __name__ == "__main__":
    from ucimlrepo import fetch_ucirepo
    from sklearn.model_selection import train_test_split

    # Busca o dataset do UCI
    zoo = fetch_ucirepo(id=111)

    # Dados
    X = zoo.data.features  # Feature matrix
    y = zoo.data.targets  # Target labels

    print(f"Total de amostras: {len(y)}")
    print("Amostras das primeiras 5 features:")
    print(X.head(5))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.4, random_state=12, shuffle=True
    )

    # Treina o classificador BNS
    bns = MultiBNS(X_train, y_train, 1000, 20, radius=7)

    for (index, feature), (index, target) in zip(
        X_test.iterrows(),
        y_test.iterrows(),
    ):
        print(bns.monitorar(feature).item(), target.item())
