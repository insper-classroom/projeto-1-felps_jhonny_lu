from DSSE import CoverageDroneSwarmSearch
import pandas as pd

env = CoverageDroneSwarmSearch(
    drone_amount=1,
    render_mode="human",
    prob_matrix_path='data/config_01.npy',
    timestep_limit=200
)

opt = {
    "drones_positions": [(18, 15)],
}

def random_policy(obs, agents):
    actions = {}
    for agent in agents:
        actions[agent] = 1
    return actions

observations, info = env.reset(options=opt)

step = 0
infos_list = []

while env.agents:
    step += 1
    actions = random_policy(observations, env.agents)
    observations, rewards, terminations, truncations, infos = env.step(actions)
    info = infos['drone0']
    info['step'] = step
    infos_list.append(info)
    print(info)

df = pd.DataFrame(infos_list)
df.to_csv('../results/data_drone_1_config_1.csv', index=False)