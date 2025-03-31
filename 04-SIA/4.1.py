from ucimlrepo import fetch_ucirepo  # type: ignore
from sklearn.model_selection import train_test_split
from bns import BNS

# Busca o dataset do UCI
zoo = fetch_ucirepo(id=111)

# Dados
X = zoo.data.features  # Feature matrix
y = zoo.data.targets  # Target labels

classes = y.iloc[:, 0].unique()


for classe in classes:
    vp, fp, vn, fn = 0, 0, 0, 0
    print(f"Classe {classe.item()}")

    bns = BNS(X, y, classe, 100, 5, 10)

    for (index, feature), (index, target) in zip(
        X.iterrows(),
        y.iterrows(),
    ):
        av = bns.monitorar(feature)
        pertence_a_classe = target.item() == classe.item()
        if av and pertence_a_classe:
            vp += 1
        elif av and not pertence_a_classe:
            fp += 1
        elif not av and pertence_a_classe:
            fn += 1
        else:
            vn += 1

    taxa_de_alarme_falso = fp / (fp + vn)
    taxa_de_deteccao = vp / (vp + fn)

    print(f"taxa de alarme falso: {int(taxa_de_alarme_falso*100)}%")
    print(f"taxa de detecção: {int(taxa_de_deteccao*100)}%")
