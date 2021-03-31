from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
import gym
import time
import numpy as np
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

def test_env(env_name : str, num_steps : int):
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False)
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    tried_actions = []
    for i in range(num_steps):
        print("i:{}".format(i))
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        if len(legal_actions) == 0:
            print("no legal actions, {}".format(tried_actions))
            print(env.env_state.attacker_obs_state.actions_tried)
            for m in env.env_state.attacker_obs_state.machines:
                print(
                    "ip: {}, shell access:{}, ssh_brute_t:{}, ftp_brute_t:{}, telnet_brute_t:{}, fs_searched:{},untried_cred:{},logged_in:{},"
                    "tools:{},backdoor:{}, flags found:{}".format(
                        m.ip, m.shell_access, m.telnet_brute_tried, m.ssh_brute_tried, m.ftp_brute_tried,
                        m.filesystem_searched, m.untried_credentials,
                        m.logged_in, m.tools_installed, m.backdoor_installed, m.flags_found))
            print("all flags?:{}".format(
                EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config)))
            print("done?:{}".format(done))

        action = np.random.choice(legal_actions)
        # if i < 1:
        #     action = 21
        # else:
        #     action = 40
        env.render()
        obs, reward, done, info = env.step(action)
        tried_actions.append(action)
        tot_rew += reward
        if EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config) and not done:
            print("All flags but done")
        if done:
            print("tot_rew:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
            tried_actions = []
            done = False
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-ctf-level-7-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-7-emulation-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-7-emulation-v3", num_steps=1000000000)
    test_env("pycr-ctf-level-7-emulation-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()