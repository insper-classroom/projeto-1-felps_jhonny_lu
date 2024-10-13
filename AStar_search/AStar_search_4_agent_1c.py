from DSSE import CoverageDroneSwarmSearch
from aigyminsper.search.Graph import State
import pandas as pd
import numpy as np


class DroneState(State):
    def __init__(self, position, prob_matrix, visited):
        self.position = position
        self.prob_matrix = prob_matrix
        self.visited = visited

    def successors(self, allow_zeros=False):
        successors = []
        x, y = self.position

        movements = {
            "Move Up": (-1, 0),
            "Move Down": (1, 0),
            "Move Left": (0, -1),
            "Move Right": (0, 1),
            "Move Up-Left": (-1, -1),
            "Move Up-Right": (-1, 1),
            "Move Down-Left": (1, -1),
            "Move Down-Right": (1, 1)
        }

        for move_name, (dx, dy) in movements.items():
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < len(self.prob_matrix) and 0 <= new_y < len(self.prob_matrix[0]):
                if allow_zeros or self.prob_matrix[new_x, new_y] > 0:
                    new_state = DroneState((new_x, new_y), self.prob_matrix, self.visited | {(new_x, new_y)})
                    successors.append(new_state)
        
        return successors

    def h(self, prob_weight=10, distance_weight=1, revisit_penalty_value=30):
        x, y = self.position
        prob_value = self.prob_matrix[x, y]

        high_prob_indices = np.argwhere(self.prob_matrix > 0)
        total_high_prob = high_prob_indices.shape[0]

        if total_high_prob == 0:
            return float('inf')

        distances = np.abs(high_prob_indices[:, 0] - x) + np.abs(high_prob_indices[:, 1] - y)
        min_distance = np.min(distances)

        max_prob = np.max(self.prob_matrix)
        normalized_prob = prob_value / max_prob if max_prob > 0 else 0

        max_distance = len(self.prob_matrix) + len(self.prob_matrix[0])
        normalized_distance = min_distance / max_distance

        revisit_penalty = 0
        if (x, y) in self.visited:
            revisit_penalty = revisit_penalty_value * (len(self.visited) / (total_high_prob + 1))

        heuristic_value = (
            -(normalized_prob * prob_weight)
            + (normalized_distance * distance_weight)
            + revisit_penalty
        )

        return heuristic_value

    def cost(self):
        return 1
    
    def description(self):
        return f"Drone na posição {self.position}"
    
    def env(self):
        return self.position
    
    def is_goal(self):
        return False

def AStar_4_agents(obs, agents, prob_matrix, visited):
    actions = {}

    for i, agent in enumerate(agents):
        current_pos = (obs[agent][0][0], obs[agent][0][1])

        drone_state = DroneState(current_pos, prob_matrix, visited[i])

        successors = drone_state.successors()

        if not successors:
            successors = drone_state.successors(allow_zeros=True)

        if not successors:
            continue

        successors.sort(key=lambda s: s.h())
        next_state = successors[0]
        next_position = next_state.position

        dx, dy = next_position[0] - current_pos[0], next_position[1] - current_pos[1]

        if dx == 1 and dy == 0:
            actions[agent] = 1
        elif dx == -1 and dy == 0:
            actions[agent] = 0
        elif dx == 0 and dy == 1:
            actions[agent] = 3
        elif dx == 0 and dy == -1:
            actions[agent] = 2
        elif dx == 1 and dy == 1:
            actions[agent] = 7
        elif dx == -1 and dy == 1:
            actions[agent] = 6
        elif dx == 1 and dy == -1:
            actions[agent] = 5
        elif dx == -1 and dy == -1:
            actions[agent] = 4

        visited[i].add(next_position)
        prob_matrix[current_pos[0], current_pos[1]] = 0

    return actions


def main():
    prob_matrix = np.load("data/config_01.npy")

    env = CoverageDroneSwarmSearch(
        drone_amount=4,
        render_mode="human",
        timestep_limit=200,
        prob_matrix_path="data/config_01.npy"
    )


    opt = {
        "drones_positions": [(15, 15), (23, 20), (31, 31), (31, 15)]
    }

    observations, info = env.reset(options=opt)

    visited = [
        set([opt['drones_positions'][0]]), 
        set([opt['drones_positions'][1]]),
        set([opt['drones_positions'][2]]),
        set([opt['drones_positions'][3]])
    ]

    step = 0
    infos_list = []

    while env.agents:
        step += 1

        actions = AStar_4_agents(observations, env.agents, prob_matrix, visited)
        observations, rewards, terminations, truncations, infos = env.step(actions)

        info = infos['drone0']
        info['step'] = step
        infos_list.append(info)


    df = pd.DataFrame(infos_list)
    df.to_csv('results/AStar_search_4_agents_1c.csv', index=False)