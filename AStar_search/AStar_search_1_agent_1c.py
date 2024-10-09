from DSSE import CoverageDroneSwarmSearch
import heapq  # Usaremos uma fila de prioridades (min-heap)
import pandas as pd
import numpy as np

# Configuração do ambiente DSSE com 1 drone e limite de movimentos (bateria)
env = CoverageDroneSwarmSearch(
    drone_amount=1,
    render_mode="human",
    prob_matrix_path='data/config_01.npy',
    timestep_limit=200
)

# Posição inicial do drone
opt = {
    "drones_positions": [(23, 23)],  # Exemplo de posição inicial
}

# Função heurística (distância Euclidiana inversa ponderada pela probabilidade)
def heuristic(current_pos, prob_matrix, prob_threshold=0.1):
    x, y = current_pos
    prob = prob_matrix[x][y]

    # Penaliza células com probabilidade muito baixa
    if prob > prob_threshold:
        return 1 / prob  # Células com maior probabilidade serão mais atrativas
    return float('inf')  # Penaliza severamente células com baixa probabilidade

# Função para obter os vizinhos válidos (8 direções)
def get_neighbors(x, y, grid_shape):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Cima, Baixo, Esquerda, Direita
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonais
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_shape[0] and 0 <= ny < grid_shape[1]:  # Verifica se está dentro dos limites
            neighbors.append((nx, ny))
    return neighbors

def a_star(initial_position, prob_matrix, battery_limit=200, prob_threshold=0.1):
    open_list = []
    heapq.heappush(open_list, (0, initial_position))  # Adiciona a posição inicial

    g_score = {initial_position: 0}
    f_score = {initial_position: heuristic(initial_position, prob_matrix, prob_threshold)}

    visited_positions = set()
    came_from = {}
    full_path = []

    for step in range(battery_limit):
        if not open_list:
            break  # Se a lista de abertos estiver vazia, encerra

        # Retira a célula com menor f(n)
        _, current_pos = heapq.heappop(open_list)

        print(f"Processando posição atual: {current_pos}")

        # Marca a célula atual como visitada e zera a probabilidade
        prob_matrix[current_pos[0], current_pos[1]] = 0
        visited_positions.add(current_pos)
        full_path.append(current_pos)  # Adiciona a posição atual ao caminho completo

        # Encontra os vizinhos válidos
        neighbors = get_neighbors(current_pos[0], current_pos[1], prob_matrix.shape)
        print(f"Vizinhos de {current_pos}: {neighbors}")

        for neighbor in neighbors:
            print(f"Verificando vizinho: {neighbor}")

            # Ignora vizinhos com baixa probabilidade
            if prob_matrix[neighbor[0], neighbor[1]] < prob_threshold:
                print(f"Pulando vizinho de baixa probabilidade: {neighbor}")
                continue

            tentative_g_score = g_score[current_pos] + (1 if (current_pos[0] == neighbor[0] or current_pos[1] == neighbor[1]) else 1.4)  # Custo fixo de 1 para movimentos laterais, 1.4 para diagonais

            # Se o vizinho não está na lista de abertos ou se encontramos um caminho melhor
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_value = tentative_g_score + heuristic(neighbor, prob_matrix, prob_threshold)
                came_from[neighbor] = current_pos  # Armazena o caminho

                # Adiciona o vizinho na lista de abertos se ele não estiver em visited_positions
                if neighbor not in visited_positions:
                    print(f"Adicionando vizinho à lista aberta: {neighbor}")
                    heapq.heappush(open_list, (f_value, neighbor))

    print(f"Caminho completo gerado: {full_path}")
    return full_path
    
def a_star_search_single_agent(agents, path, indice_path, obs):
    actions = {}
    movie = path[indice_path]

    for agent in agents:
        current_pos = obs[agent][0]

        if current_pos == movie:
            actions[agent] = 8  # Parar
        else:
            delta_x = movie[0] - current_pos[0]
            delta_y = movie[1] - current_pos[1]

            # Lógica de movimento considerando diagonais
            if abs(delta_x) == 1 and abs(delta_y) == 1:  # Movimento diagonal
                if delta_x < 0 and delta_y > 0:
                    actions[agent] = 5  # Mover diagonal cima-direita
                elif delta_x < 0 and delta_y < 0:
                    actions[agent] = 4  # Mover diagonal cima-esquerda
                elif delta_x > 0 and delta_y < 0:
                    actions[agent] = 6  # Mover diagonal baixo-esquerda
                elif delta_x > 0 and delta_y > 0:
                    actions[agent] = 7  # Mover diagonal baixo-direita
            elif abs(delta_x) > abs(delta_y):  # Movimento prioritário na direção vertical
                if delta_x < 0:
                    actions[agent] = 2  # Mover para cima
                else:
                    actions[agent] = 3  # Mover para baixo
            else:  # Movimento prioritário na direção horizontal
                if delta_y < 0:
                    actions[agent] = 0  # Mover para a esquerda
                else:
                    actions[agent] = 1  # Mover para a direita

    return actions

# Inicializa a simulação
observations, info = env.reset(options=opt)

# Variáveis de controle da simulação
step = 0
infos_list = []
path = a_star(observations["drone0"][0], observations["drone0"][1], battery_limit=200)
indice = 0

# Loop de simulação com o algoritmo A*
while env.agents:
    step += 1
    # Executa o algoritmo A* para determinar as melhores ações
    actions = a_star_search_single_agent(env.agents, path, indice, observations)
    observations, rewards, terminations, truncations, infos = env.step(actions)
    info = infos['drone0']
    info['step'] = step
    infos_list.append(info)
    indice += 1

# Salva os resultados em um arquivo CSV
df = pd.DataFrame(infos_list)
df.to_csv('results/a_star_search_1_agent.csv', index=False)