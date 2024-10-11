from DSSE import CoverageDroneSwarmSearch
import pandas as pd

env = CoverageDroneSwarmSearch(
    drone_amount=2,
    render_mode="human",
    prob_matrix_path='data/config_01.npy',
    timestep_limit=200
)

opt = {
    "drones_positions": [(23, 14), (24, 14)],
}

def traditional_search_single_agent(obs, agents, opt):

    actions = {}
    
    for agent in agents:
        if agent == "drone0":
            start_position = (opt['drones_positions'][0][0], opt['drones_positions'][0][1])

            if (obs[agent][0][0] - start_position[0]) % 2 == 0:
                if obs[agent][0][1] == len(obs[agent][1]) - start_position[1] -1:
                    actions[agent] = 0
                else:
                    actions[agent] = 3
            elif (obs[agent][0][0] - start_position[0]) % 2 != 0:
                if obs[agent][0][1] == start_position[1] + 1:
                    actions[agent] = 0
                else:
                    actions[agent] = 2
        elif agent == "drone1":
            start_position = (opt['drones_positions'][1][0], opt['drones_positions'][1][1])
            
            if (obs[agent][0][0] - start_position[0]) % 2 == 0:
                if obs[agent][0][1] == len(obs[agent][1]) - start_position[1] -1:
                    actions[agent] = 1
                else:
                    actions[agent] = 3
            elif (obs[agent][0][0] - start_position[0]) % 2 != 0:
                if obs[agent][0][1] == start_position[1] + 1:
                    actions[agent] = 1
                else:
                    actions[agent] = 2

    return actions

observations, info = env.reset(options=opt)

step = 0
infos_list = []

while env.agents:
    step += 1
    actions = traditional_search_single_agent(observations, env.agents, opt)
    observations, rewards, terminations, truncations, infos = env.step(actions)
    info = infos['drone0']
    #print(observations['drone0'][0])
    info['step'] = step
    infos_list.append(info)
    #print(info)

df = pd.DataFrame(infos_list)
df.to_csv('results/traditional_search_2_agent_1c.csv', index=False)