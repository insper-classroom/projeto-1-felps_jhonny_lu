from DSSE import CoverageDroneSwarmSearch
from aigyminsper.search.Graph import State
import pandas as pd
import numpy as np


prob_matrix = np.load("data/config_02.npy" )

# Inicializar o ambiente DSSE
env = CoverageDroneSwarmSearch(
    drone_amount=1,
    render_mode="human",
    timestep_limit=200,
    prob_matrix_path="data/config_02.npy" 
)

starting_position = (32, 32)
opt = {
    "drones_positions": [starting_position],
}

observations, info = env.reset(options=opt)

# Classe DroneState com controle de sucessores
class DroneState(State):
    def __init__(self, position, prob_matrix, visited):
        self.position = position
        self.prob_matrix = prob_matrix
        self.visited = visited

    def successors(self, allow_zeros=False):
        successors = []
        x, y = self.position
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.prob_matrix) and 0 <= new_y < len(self.prob_matrix[0]):
                if allow_zeros or self.prob_matrix[new_x, new_y] > 0:
                    new_state = DroneState((new_x, new_y), self.prob_matrix, self.visited | {(new_x, new_y)})
                    successors.append(new_state)
        
        return successors

    def h(self, prob_weight=10, distance_weight=1, revisit_penalty_value=30):
        x, y = self.position
        prob_value = self.prob_matrix[x, y]
        
        # Calculate Manhattan distance to the nearest high-probability cell
        high_prob_indices = np.argwhere(self.prob_matrix > 0)
        total_high_prob = high_prob_indices.shape[0]
        
        if total_high_prob == 0:
            return float('inf')  # No high-probability cells left
        
        distances = np.abs(high_prob_indices[:, 0] - x) + np.abs(high_prob_indices[:, 1] - y)
        min_distance = np.min(distances)
        
        # Normalize probability and distance
        normalized_prob = prob_value / np.max(self.prob_matrix) if np.max(self.prob_matrix) > 0 else 0
        normalized_distance = min_distance / (len(self.prob_matrix) + len(self.prob_matrix[0]))
        
        # Heuristic: prioritize high probability and proximity
        revisit_penalty = revisit_penalty_value if (x, y) in self.visited else 0
        heuristic_value = -(normalized_prob * prob_weight) + (normalized_distance * distance_weight) + revisit_penalty
        
        return heuristic_value


    def cost(self):
        return 1  # Maintain a consistent cost for each move
    
    def description(self):
        return f"Drone na posição {self.position}"
    
    def env(self):
        return self.position
    
    def is_goal(self):
        return False


def AStar_single_agent(current_pos, next_pos):
    dx, dy = next_pos[0] - current_pos[0], next_pos[1] - current_pos[1]
    if dx == 1 and dy == 0:
        return 1  # Direita
    elif dx == -1 and dy == 0:
        return 0  # Esquerda
    elif dx == 0 and dy == 1:
        return 3  # Baixo
    elif dx == 0 and dy == -1:
        return 2  # Cima
    elif dx == 1 and dy == 1:
        return 7  # Diagonal direita para baixo
    elif dx == -1 and dy == 1:
        return 6  # Diagonal esquerda para baixo
    elif dx == 1 and dy == -1:
        return 5  # Diagonal direita para cima
    elif dx == -1 and dy == -1:
        return 4  # Diagonal esquerda para cima
    return 8  # Não fazer nada


visited = {(23, 23)}  # Posição inicial já visitada
current_position = starting_position
drone_state = DroneState(starting_position, prob_matrix, visited)

step_limit = 200  # Limite de passos
step = 0
infos_list = []

while step < step_limit:
    # Obter sucessores e escolher o de maior probabilidade
    successors = drone_state.successors()

    if not successors:
        # Se não houver sucessores com probabilidade > 0, permitimos zeros
        successors = drone_state.successors(allow_zeros=True)

    if not successors:
        # Se mesmo assim não houver sucessores, termina a exploração
        break

    # Ordenar sucessores pela heurística de maior probabilidade
    successors.sort(key=lambda s: s.h())

    # Escolher o sucessor com a maior probabilidade
    next_state = successors[0]
    next_position = next_state.position

    # Realizar a ação no ambiente DSSE
    action = AStar_single_agent(current_position, next_position)
    actions = {'drone0': action}
    observations, rewards, terminations, truncations, infos = env.step(actions)

    # Zera a probabilidade da célula atual para evitar revisitá-la
    x, y = current_position
    prob_matrix[x, y] = 0

    print(f"{step} - Movendo para {next_position}, Ação: {action}, Probabilidade: {1 - next_state.h()}")

    # Atualizar posição e estado do drone
    current_position = next_position
    drone_state = next_state
    step += 1

    info = infos['drone0']
    #print(observations['drone0'][0])
    info['step'] = step
    infos_list.append(info)

# Fechar o ambiente DSSE após a execução
env.close()

# Salvar os resultados em um arquivo CSV
df = pd.DataFrame(infos_list)
df.to_csv('results/AStar_search_1_agent_2c.csv', index=False)