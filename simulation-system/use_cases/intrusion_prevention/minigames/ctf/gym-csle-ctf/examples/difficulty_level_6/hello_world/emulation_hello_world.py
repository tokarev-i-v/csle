from csle_common.dao.network.emulation_config import EmulationConfig
import gym
import numpy as np


def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.6.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.6.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.6.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False,
                                     port_forward_next_port=5650)
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        print(i)
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        tot_rew += reward
        #env.render()
        if done:
            print("tot_rew:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    test_env("csle-ctf-level-6-emulation-v4", num_steps=1000000000)

if __name__ == '__main__':
    test_all()