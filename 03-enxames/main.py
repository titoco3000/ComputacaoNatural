from visualizacao_particulas import VisualizacaoParticulas, lerp
import random


vies_social = 2
vies_cognitivo = 3
inercia = 0.98


def fn(x, y):
    x = x * 4 - 2
    y = y * 4 - 2
    return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2


def atualizar_individuos(individuos):
    melhor_individuo = max(individuos, key=lambda i: i.val)

    # atualiza o peso para cada individuo
    for i in individuos:
        r1 = random.random()
        r2 = random.random()
        nova_vel = (
            inercia * i.vel[0]
            + r1 * vies_cognitivo * (i.melhor_pos[0] - i.pos[0])
            + r2 * vies_social * (melhor_individuo.pos[0] - i.pos[0]),
            inercia * i.vel[1]
            + r1 * vies_cognitivo * (i.melhor_pos[1] - i.pos[1])
            + r2 * vies_social * (melhor_individuo.pos[1] - i.pos[1]),
        )
        i.vel = nova_vel
        i.pos = lerp(i.pos, (i.pos[0] + i.vel[0], i.pos[1] + i.vel[1]), 0.01)
        i.pos = min(1, max(0, i.pos[0])), min(1, max(0, i.pos[1]))
        i.val = fn(*i.pos)
        if i.val > fn(*i.melhor_pos):
            i.melhor_pos = i.pos


if __name__ == "__main__":
    viz = VisualizacaoParticulas(10, 0.1)

    viz.loop(atualizar_individuos)
