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
                    #print(f"{move_name}: Nova posição ({new_x}, {new_y}) adicionada.")
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


def AStar_single_agent(current_pos, next_pos, agents):
    actions = {}

    for agent in agents:
        dx, dy = next_pos[0] - current_pos[0], next_pos[1] - current_pos[1]
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
        else:
            actions[agent] = 8 
    
    return actions


def main():
    prob_matrix = np.load("data/config_01.npy" )

    env = CoverageDroneSwarmSearch(
        drone_amount=1,
        render_mode="human",
        timestep_limit=200,
        prob_matrix_path="data/config_01.npy" 
    )

    starting_position = (23, 23)

    opt = {
        "drones_positions": [starting_position],
    }

    observations, info = env.reset(options=opt)


    visited = {starting_position} 
    current_position = starting_position
    drone_state = DroneState(starting_position, prob_matrix, visited)

    step = 0
    infos_list = []

    while env.agents:
        successors = drone_state.successors()

        if not successors:
            successors = drone_state.successors(allow_zeros=True)

        if not successors:
            break

        successors.sort(key=lambda s: s.h())

        next_state = successors[0]
        next_position = next_state.position

        actions = AStar_single_agent(current_position, next_position, env.agents)
        observations, rewards, terminations, truncations, infos = env.step(actions)

        x, y = current_position
        prob_matrix[x, y] = 0

        current_position = next_position
        drone_state = next_state
        step += 1

        info = infos['drone0']
        #print(observations['drone0'][0])
        info['step'] = step
        infos_list.append(info)

    df = pd.DataFrame(infos_list)
    df.to_csv('results/AStar_search_1_agent_1c.csv', index=False)