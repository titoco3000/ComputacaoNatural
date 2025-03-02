import random

# implementacao algoritmo genetico

def algoritmo_genetico(func_gene_aleatorio, func_avaliadora, tamanho_genoma, func_correcao=None, pop=100, mut_rate=0.01, geracoes=100, minimizar=False):
    def escolher_progenitores(pontuacoes):
        if minimizar:
            pior = max(pontuacoes)
            pontuacoes = [pior+1-x for x in pontuacoes]
        
        p = [None, None]
        total = sum(pontuacoes)
        while p[0] is None or p[1] is None or p[1] == p[0]:
            escolha = random.random() * total
            soma = 0
            for i in range(len(pontuacoes)):
                soma+=pontuacoes[i]
                if escolha<soma:
                    if p[0] is None:
                        p[0] = i
                    else:
                        p[1] = i
                    break
        return p
    
    def reproduzir(pai, mae):
        particao = random.randint(0, len(pai)-1)
        filhos = [[],[]]
        # Produz os filhos
        for i in range(len(pai)):
            if i <particao:
                filhos[0].append(pai[i])
                filhos[1].append(mae[i])
            else:
                filhos[1].append(pai[i])
                filhos[0].append(mae[i])
        
        # Causa mutacoes
        for filho in filhos:
            for i in range(len(filho)):
                if random.random()<mut_rate:
                    filho[i] = func_gene_aleatorio()
            if func_correcao:
                func_correcao(filho)

        return filhos
        

    # gera populacao inicial aleatoria
    populacao = [[func_gene_aleatorio() for _ in range(tamanho_genoma)] for _ in range(pop)]

    if func_correcao:
        for p in populacao:
            func_correcao(p)

    melhor_pontuacao = -1
    melhor = []

    melhor_por_geracao = []
    
    for geracao in range(geracoes):
        pontuacoes = [func_avaliadora(genoma) for genoma in populacao]
        index_melhor = (min if minimizar else max)(range(len(pontuacoes)), key=pontuacoes.__getitem__)
        melhor_por_geracao.append(pontuacoes[index_melhor])

        if pontuacoes[index_melhor] > melhor_pontuacao:
            melhor_pontuacao = pontuacoes[index_melhor]
            melhor = populacao[index_melhor]

        populacao = [
            ind for p in [
                escolher_progenitores(pontuacoes) for _ in range(pop)
            ] for ind in reproduzir(populacao[p[0]], populacao[p[1]])
        ]

    pontuacoes = [func_avaliadora(genoma) for genoma in populacao]
    index_melhor = (min if minimizar else max)(range(len(pontuacoes)), key=pontuacoes.__getitem__)
    if pontuacoes[index_melhor] > melhor_pontuacao:
        melhor_pontuacao = pontuacoes[index_melhor]
        melhor = populacao[index_melhor]

    return {
        "melhor":melhor, 
        "pontuacao_por_geracao":melhor_por_geracao, 
        "pontuacao":melhor_pontuacao,
        "pop":pop,
        "mut_rate":mut_rate,
        "geracoes":geracoes,
        "target": "min" if minimizar else "max"
    }

current_index = 0

def plot(resultados):
    global current_index
    import matplotlib.pyplot as plt
    import matplotlib.widgets as widgets

    if type(resultados) != list:
        resultados = [resultados]

    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(bottom=0.2)

    current_index = 0

    # Initial plot
    def plot_data(index):
        ax.clear()
        ax.plot(resultados[index]["pontuacao_por_geracao"], label=f'pontuação ({resultados[index]["target"]}: {(max if resultados[index]["target"]=="max" else min)(resultados[index]["pontuacao_por_geracao"])})')
        ax.set_xlabel('Gerações')
        ax.set_ylabel('Pontuação')
        ax.set_title(f'Evolução da Pontuação - População {resultados[index]["pop"]}, Mutação {resultados[index]["mut_rate"]}, Gerações {resultados[index]["geracoes"]}')
        ax.legend()
        ax.grid()
        fig.canvas.draw()

    plot_data(current_index)

    # Button callback functions
    def next_plot(event):
        global current_index
        current_index = min(current_index + 1,len(resultados)-1) 
        plot_data(current_index)

    def prev_plot(event):
        global current_index
        current_index = max(current_index - 1, 0)
        plot_data(current_index)

    if len(resultados) > 1:

        # Add navigation buttons
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        btn_next = widgets.Button(axnext, 'Next')
        btn_prev = widgets.Button(axprev, 'Previous')
        btn_next.on_clicked(next_plot)
        btn_prev.on_clicked(prev_plot)

    plt.show()

