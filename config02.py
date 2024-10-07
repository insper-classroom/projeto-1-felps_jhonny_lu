from DSSE import CoverageDroneSwarmSearch

env = CoverageDroneSwarmSearch(
    drone_amount=1,
    render_mode="human",
    prob_matrix_path='data/config_02.npy',
    timestep_limit=100
)

opt = {
    "drones_positions": [(0, 0)],
}

def random_policy(obs, agents):
    actions = {}
    for agent in agents:
        actions[agent] = env.action_space(agent).sample()
    return actions

observations, info = env.reset(options=opt)

step = 0
while env.agents:
    step += 1
    actions = random_policy(observations, env.agents)
    observations, rewards, terminations, truncations, infos = env.step(actions)
    print(infos)