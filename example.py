from DSSE import CoverageDroneSwarmSearch

env = CoverageDroneSwarmSearch(
    drone_amount=3,
    render_mode="human",
    disaster_position=(-24.02, -46.10),  # (lat, long) some place near Florianópolis
    pre_render_time=2, # hours to simulate
    timestep_limit=100,
)

opt = {
    "drones_positions": [(10,10),(20, 20),(30,30)],
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
    print(f'{step} - {infos}')