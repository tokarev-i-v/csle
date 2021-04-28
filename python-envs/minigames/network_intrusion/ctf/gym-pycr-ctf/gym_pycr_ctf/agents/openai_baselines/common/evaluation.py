import typing
from typing import Callable, List, Optional, Tuple, Union

import gym
import numpy as np
import time
from gym_pycr_ctf.agents.openai_baselines.common.vec_env import VecEnv
from gym_pycr_ctf.dao.network.env_config import EnvConfig

if typing.TYPE_CHECKING:
    from gym_pycr_ctf.agents.openai_baselines.common.base_class import BaseAlgorithm
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from gym_pycr_ctf.dao.agent.train_mode import TrainMode
from gym_pycr_ctf.dao.agent.train_agent_log_dto import TrainAgentLogDTO

def evaluate_policy(model: "BaseAlgorithm", env: Union[gym.Env, VecEnv], env_2: Union[gym.Env, VecEnv],
                    n_eval_episodes : int=10,
                    deterministic : bool= True,
                    render : bool =False, callback: Optional[Callable] = None,
                    reward_threshold: Optional[float] = None,
                    return_episode_rewards: bool = False, attacker_agent_config : AgentConfig = None,
                    train_episode = 1, env_config = None, env_configs = None):
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param env_2: (gym.Env or VecEnv) The second gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (bool) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when ``return_episode_rewards`` is True
    """
    eval_mean_reward, eval_std_reward = -1, -1
    train_eval_mean_reward, train_eval_std_reward = _eval_helper(env=env, attacker_agent_config=attacker_agent_config,
                                                                 n_eval_episodes=n_eval_episodes,
                                                                 deterministic=deterministic,
                                                                 callback=callback, train_episode=train_episode,
                                                                 model=model, env_config=env_config,
                                                                 env_configs=env_configs)

    if env_2 is not None:
        randomize_starting_states = []
        for i in range(env_2.num_envs):
            randomize_starting_states.append(env_2.envs[i].env_config.randomize_attacker_starting_state)
            env_2.envs[i].env_config.randomize_attacker_starting_state = False

        eval_mean_reward, eval_std_reward = _eval_helper(
            env=env_2, attacker_agent_config=attacker_agent_config, n_eval_episodes=n_eval_episodes,  deterministic=deterministic,
            callback=callback, train_episode=train_episode, model=model, env_config=env_config,
            env_configs=env_configs)

        for i in range(env_2.num_envs):
            env_2.envs[i].env_config.randomize_attacker_starting_state = randomize_starting_states[i]
    return train_eval_mean_reward, train_eval_std_reward, eval_mean_reward, eval_std_reward


def _eval_helper(env, attacker_agent_config: AgentConfig, model, n_eval_episodes, deterministic,
                 callback, train_episode, env_config, env_configs):
    attacker_agent_config.logger.info("Starting Evaluation")

    model.num_eval_episodes = 0
    if attacker_agent_config.eval_episodes < 1:
        return

    done = False
    state = None

    # Tracking metrics
    episode_rewards = []
    episode_steps = []
    episode_flags = []
    episode_flags_percentage = []
    eval_episode_rewards_env_specific = {}
    eval_episode_steps_env_specific = {}
    eval_episode_flags_env_specific = {}
    eval_episode_flags_percentage_env_specific = {}

    if env.num_envs == 1 and not isinstance(env, SubprocVecEnv):
        env.envs[0].enabled = True
        env.envs[0].stats_recorder.closed = False
        env.envs[0].episode_id = 0


    for episode in range(n_eval_episodes):
        infos = np.array([{"non_legal_actions": env.initial_illegal_actions} for i in range(env.num_envs)])

        for i in range(env.num_envs):
            if env_configs is not None:
                if i < len(env_configs):
                    env_conf = env_configs[i]
                else:
                    env_conf = env_configs[0]
            else:
                env_conf = env_config
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
            done = False
            state = None
            env_state = None
            episode_reward = 0.0
            episode_length = 0
            time_str = str(time.time())
            while not done:
                if isinstance(env, DummyVecEnv):
                    env_state = env.envs[i].env_state

                if env.num_envs == 1 and not isinstance(env, SubprocVecEnv) and attacker_agent_config.eval_render:
                    time.sleep(1)
                    env.render()

                actions, state = model.predict(obs, state=state, deterministic=deterministic, infos=infos,
                                               env_config=env_conf,
                                               env_configs=env_configs, env=env, env_idx=i,
                                               env_state=env_state)
                action = actions[0]
                if isinstance(env, SubprocVecEnv):
                    obs, reward, done, _info = env.eval_step(action, idx=i)
                elif isinstance(env, DummyVecEnv):
                    obs, reward, done, _info = env.envs[i].step(action)
                infos = [_info]
                episode_reward += reward
                episode_length += 1

            # Render final frame when game completed
            if env.num_envs == 1 and attacker_agent_config.eval_render:
                env.render()

            # Record episode metrics
            episode_rewards.append(episode_reward)
            episode_steps.append(episode_length)
            episode_flags.append(_info["flags"])
            episode_flags_percentage.append(_info["flags"] / env_conf.num_flags)
            eval_episode_rewards_env_specific, eval_episode_steps_env_specific, \
            eval_episode_flags_env_specific, eval_episode_flags_percentage_env_specific = \
                eval_update_env_specific_metrics(env_conf, eval_episode_rewards_env_specific,
                                                 eval_episode_steps_env_specific, eval_episode_flags_env_specific,
                                                 eval_episode_flags_percentage_env_specific, episode_reward, episode_length,
                                                 _info, i)

            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
            if env.num_envs == 1:
                env.close()

            # Update eval stats
            model.num_eval_episodes += 1
            model.num_eval_episodes_total += 1


            # Save gifs
            if env.num_envs == 1 and not isinstance(env, SubprocVecEnv) and attacker_agent_config.gifs or attacker_agent_config.video:
                # Add frames to tensorboard
                for idx, frame in enumerate(env.envs[0].episode_frames):
                    model.tensorboard_writer.add_image(str(train_episode) + "_eval_frames/" + str(idx),
                                                       frame, global_step=train_episode,
                                                       dataformats="HWC")

                # Save Gif
                env.envs[0].generate_gif(attacker_agent_config.gif_dir + "episode_" + str(train_episode) + "_"
                                         + time_str + ".gif", attacker_agent_config.video_fps)
        # Log average metrics every <self.config.eval_log_frequency> episodes
        if episode % attacker_agent_config.eval_log_frequency == 0:
            model.log_metrics_attacker(iteration=episode, result=model.eval_result, episode_rewards=episode_rewards,
                                       episode_steps=episode_steps, eval=True, episode_flags=episode_flags,
                                       episode_flags_percentage=episode_flags_percentage)

    # Log average eval statistics
    model.log_metrics_attacker(iteration=train_episode, result=model.eval_result, episode_rewards=episode_rewards,
                               episode_steps=episode_steps, eval=True, episode_flags=episode_flags,
                               episode_flags_percentage=episode_flags_percentage)

    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    attacker_agent_config.logger.info("Evaluation Complete")
    print("Evaluation Complete")
    # env.close()
    # env.reset()
    return mean_reward, std_reward


def quick_evaluate_policy(attacker_model: "BaseAlgorithm", defender_model: "BaseAlgorithm",
                          env: Union[gym.Env, VecEnv], env_2: Union[gym.Env, VecEnv],
                          n_eval_episodes_train : int=10, n_eval_episodes_eval2 : int=10,
                          deterministic : bool= True, attacker_agent_config : AgentConfig = None,
                          defender_agent_config : AgentConfig = None,
                          env_config: EnvConfig = None, env_configs : List[EnvConfig] = None,
                          eval_env_config: EnvConfig = None, eval_envs_configs: List[EnvConfig] = None,
                          train_mode: TrainMode = TrainMode.TRAIN_ATTACKER,
                          train_dto : TrainAgentLogDTO = None
                          ):
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param attacker_model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes_train: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param attacker_agent_config: agent config
    :return: episode_rewards, episode_steps, episode_flags_percentage, episode_flags
    """
    randomize_starting_states = []
    simulate_snort = []
    for i in range(env.num_envs):
        if isinstance(env, DummyVecEnv):
            randomize_starting_states.append(env.envs[i].env_config.randomize_attacker_starting_state)
            simulate_snort.append(env.envs[i].env_config.snort_baseline_simulate)
            env.envs[i].env_config.randomize_attacker_starting_state = False
            env.envs[i].env_config.snort_baseline_simulate = False
        elif isinstance(env, SubprocVecEnv):
            randomize_starting_states = env.get_randomize_starting_state()
            simulate_snort = env.get_snort_baseline_simulate()
            env.set_randomize_starting_state(False)
            env.set_snort_baseline_simulate(False)


    train_dto = _quick_eval_helper(
        env=env, attacker_model=attacker_model, defender_model=defender_model,
        n_eval_episodes=n_eval_episodes_train, deterministic=deterministic, env_config=env_config, train_mode=train_mode,
        env_configs =env_configs,
        train_log_dto=train_dto, eval_2=False)

    for i in range(env.num_envs):
        if isinstance(env, DummyVecEnv):
            env.envs[i].env_config.randomize_attacker_starting_state = randomize_starting_states[i]
            env.envs[i].env_config.snort_baseline_simulate = simulate_snort[i]
        elif isinstance(env, SubprocVecEnv):
            env.set_randomize_starting_state(randomize_starting_states[0])
            env.set_snort_baseline_simulate(simulate_snort[0])

    if env_2 is not None:
        randomize_starting_states = []
        simulate_snort = []
        for i in range(env_2.num_envs):
            if isinstance(env, DummyVecEnv):
                randomize_starting_states.append(env_2.envs[i].env_config.randomize_attacker_starting_state)
                simulate_snort.append(env_2.envs[i].env_config.snort_baseline_simulate)
                env_2.envs[i].env_config.randomize_attacker_starting_state = False
                env_2.envs[i].env_config.snort_baseline_simulate = False
            elif isinstance(env, SubprocVecEnv):
                randomize_starting_states = env_2.get_randomize_starting_state()
                simulate_snort = env_2.get_snort_baseline_simulate()
                env_2.set_randomize_starting_state(False)
                env_2.set_snort_baseline_simulate(False)

        train_dto = _quick_eval_helper(
            env=env_2, attacker_model=attacker_model, defender_model=defender_model,
            n_eval_episodes=n_eval_episodes_eval2, deterministic=deterministic, env_config=eval_env_config,
            train_mode=train_mode,
            env_configs=eval_envs_configs,
            emulation_env=True, eval_2=True, train_log_dto=train_dto
        )
        for i in range(env_2.num_envs):
            if isinstance(env, DummyVecEnv):
                env_2.envs[i].env_config.randomize_attacker_starting_state = randomize_starting_states[i]
                env_2.envs[i].env_config.snort_baseline_simulate = simulate_snort[i]
            elif isinstance(env, SubprocVecEnv):
                env_2.set_randomize_starting_state(randomize_starting_states[0])
                env_2.set_snort_baseline_simulate(simulate_snort[0])

    return train_dto


def _quick_eval_helper(env, attacker_model, defender_model,
                       n_eval_episodes, deterministic, env_config, train_mode, env_configs = None,
                       emulation_env : bool = False,
                       train_log_dto : TrainAgentLogDTO = None, eval_2 : bool = False):

    for episode in range(n_eval_episodes):
        if isinstance(env, SubprocVecEnv):
            infos = np.array([{"attacker_non_legal_actions": env.attacker_initial_illegal_actions,
                               "defender_non_legal_actions": env.defender_initial_illegal_actions
                               } for i in range(env.num_envs)])
        elif isinstance(env, DummyVecEnv):
            infos = np.array([{"attacker_non_legal_actions": env.envs[i].attacker_initial_illegal_actions,
                               "defender_non_legal_actions": env.envs[i].defender_initial_illegal_actions
                               } for i in range(env.num_envs)])
        for i in range(env.num_envs):
            if env_configs is not None:
                env_conf = env_configs[i]
            else:
                env_conf = env_config
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
                env_conf = env.env_config(i)
                env_configs = env.env_configs()
            done = False
            state = None
            env_state = None
            attacker_episode_reward = 0.0
            defender_episode_reward = 0.0
            episode_length = 0
            while not done:
                if isinstance(env, DummyVecEnv):
                    env_state = env.envs[i].env_state
                    agent_state = env.envs[i].attacker_agent_state
                if isinstance(obs, list):
                    obs_attacker, obs_defender = obs[0]
                else:
                    obs_attacker, obs_defender = obs
                attacker_actions = None
                defender_actions = [None]
                if train_mode == train_mode.TRAIN_ATTACKER or train_mode == train_mode.SELF_PLAY:
                    attacker_actions, state = attacker_model.predict(np.array([obs_attacker]), state=state,
                                                                     deterministic=deterministic,
                                                                     infos=infos,
                                                                     env_config = env_conf,
                                                                     env_configs=env_configs, env=env, env_idx=i,
                                                                     env_state=env_state,
                                                                     attacker=True)
                if train_mode == train_mode.TRAIN_DEFENDER or train_mode == train_mode.SELF_PLAY:
                    defender_actions, state = defender_model.predict(np.array([obs_defender]), state=state,
                                                                     deterministic=deterministic,
                                                                     infos=infos,
                                                                     env_config=env_conf,
                                                                     env_configs=env_configs, env=env, env_idx=i,
                                                                     env_state=env_state,
                                                                     attacker=False)
                    if attacker_actions is None:
                        attacker_actions = np.array([None])
                defender_action = defender_actions[0]
                attacker_action = attacker_actions[0]
                action = (attacker_action, defender_action)
                # if emulation_env:
                #     print("taking eval step in emulation: {}".format(action))
                if isinstance(env, SubprocVecEnv):
                    obs, reward, done, _info = env.eval_step(action, idx=i)
                elif isinstance(env, DummyVecEnv):
                    obs, reward, done, _info = env.envs[i].step(action)
                # if emulation_env:
                #     print("eval step in emulation complete")
                attacker_reward, defender_reward = reward
                infos = [_info]
                attacker_episode_reward += attacker_reward
                defender_episode_reward += defender_reward
                episode_length += 1

            # Record episode metrics
            if not eval_2:
                train_log_dto.attacker_eval_episode_rewards.append(attacker_episode_reward)
                train_log_dto.defender_eval_episode_rewards.append(defender_episode_reward)
                train_log_dto.eval_episode_steps.append(episode_length)
                train_log_dto.eval_episode_flags.append(_info["flags"])
                train_log_dto.eval_episode_caught.append(_info["caught_attacker"])
                train_log_dto.eval_episode_early_stopped.append(_info["early_stopped"])
                train_log_dto.eval_episode_successful_intrusion.append(_info["successful_intrusion"])
                train_log_dto.eval_episode_snort_severe_baseline_rewards.append(_info["snort_severe_baseline_reward"])
                train_log_dto.eval_episode_snort_warning_baseline_rewards.append(_info["snort_warning_baseline_reward"])
                train_log_dto.eval_episode_snort_critical_baseline_rewards.append(_info["snort_critical_baseline_reward"])
                train_log_dto.eval_episode_var_log_baseline_rewards.append(_info["var_log_baseline_reward"])
                train_log_dto.eval_episode_flags_percentage.append(_info["flags"] / env_conf.num_flags)
                train_log_dto.eval_attacker_action_costs.append(_info["attacker_cost"])
                train_log_dto.eval_attacker_action_costs_norm.append(_info["attacker_cost_norm"])
                train_log_dto.eval_attacker_action_alerts.append(_info["attacker_alerts"])
                train_log_dto.eval_attacker_action_alerts_norm.append(_info["attacker_alerts_norm"])
                train_log_dto.eval_update_env_specific_metrics(env_conf, _info, i)
            else:
                train_log_dto.attacker_eval_2_episode_rewards.append(attacker_episode_reward)
                train_log_dto.defender_eval_2_episode_rewards.append(defender_episode_reward)
                train_log_dto.eval_2_episode_steps.append(episode_length)
                train_log_dto.eval_2_episode_flags.append(_info["flags"])
                train_log_dto.eval_2_episode_caught.append(_info["caught_attacker"])
                train_log_dto.eval_2_episode_early_stopped.append(_info["early_stopped"])
                train_log_dto.eval_2_episode_successful_intrusion.append(_info["successful_intrusion"])
                train_log_dto.eval_2_episode_snort_severe_baseline_rewards.append(_info["snort_severe_baseline_reward"])
                train_log_dto.eval_2_episode_snort_warning_baseline_rewards.append(_info["snort_warning_baseline_reward"])
                train_log_dto.eval_2_episode_snort_critical_baseline_rewards.append(
                    _info["snort_critical_baseline_reward"])
                train_log_dto.eval_2_episode_var_log_baseline_rewards.append(_info["var_log_baseline_reward"])
                train_log_dto.eval_2_episode_flags_percentage.append(_info["flags"] / env_conf.num_flags)
                train_log_dto.eval_2_attacker_action_costs.append(_info["attacker_cost"])
                train_log_dto.eval_2_attacker_action_costs_norm.append(_info["attacker_cost_norm"])
                train_log_dto.eval_2_attacker_action_alerts.append(_info["attacker_alerts"])
                train_log_dto.eval_2_attacker_action_alerts_norm.append(_info["attacker_alerts_norm"])
                train_log_dto.eval_2_update_env_specific_metrics(env_conf, _info, i)
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
                env_conf = env.env_config(i)
                env_configs = env.env_configs()
    return train_log_dto
