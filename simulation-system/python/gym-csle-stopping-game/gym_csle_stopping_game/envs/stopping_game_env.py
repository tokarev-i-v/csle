from typing import Tuple, Dict, Union, List
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_system_identification.emulator import Emulator
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_state import StoppingGameState
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions


class StoppingGameEnv(BaseEnv):
    """
    OpenAI Gym Env for the csle-stopping-game
    """

    def __init__(self, config: StoppingGameConfig):
        self.config = config

        # Initialize environment state
        self.state = StoppingGameState(b1=self.config.b1, L=self.config.L)

        # Setup spaces
        self.attacker_observation_space = self.config.attacker_observation_space()
        self.defender_observation_space = self.config.defender_observation_space()
        self.attacker_action_space = self.config.attacker_action_space()
        self.defender_action_space = self.config.defender_action_space()

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        # Setup traces
        self.traces = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, action_profile : Tuple[int, np.ndarray]) \
            -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[int, int], bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, done, info)
        """

        # Setup initial values
        a1, pi2 = action_profile
        assert pi2.shape[0] == len(self.config.S)
        assert pi2.shape[1] == len(self.config.A1)
        done = False
        info = {}

        # Compute r, s', b',o'
        a2 = StoppingGameUtil.sample_attacker_action(pi2 = pi2, s=self.state.s)
        r = self.config.R[self.state.l - 1][a1][a2][self.state.s]
        self.state.s = StoppingGameUtil.sample_next_state(l=self.state.l, a1=a1, a2=a2,
                                                          T=self.config.T,
                                                          S=self.config.S, s=self.state.s)
        o = max(self.config.O)
        if self.state.s == 2:
            done = True
        else:
            o = StoppingGameUtil.sample_next_observation(Z=self.config.Z,
                                                         O=self.config.O, s_prime=self.state.s)
            self.state.b = StoppingGameUtil.next_belief(o=o, a1=a1, b=self.state.b, pi2=pi2,
                                                        config=self.config,
                                                        l=self.state.l, a2=a2)

        # Update stops remaining
        self.state.l = self.state.l-a1
        info["l"] = self.state.l
        info["s"] = self.state.s
        info["a1"] = a1
        info["a2"] = a2
        info["o"] = o

        # Get observations
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.state.s)
        self.trace.beliefs.append(self.state.b[1])
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
            self.trace.defender_observations.append(defender_obs)
        else:
            info = self._final_info(info)

        return (defender_obs, attacker_obs), (r,-r), done, info

    def _final_info(self, info) -> Dict[str, Union[float, int]]:
        """
        Adds the cumulative reward and episode length to the info dict
        :param info: the info dict to update
        :return: the updated info dict
        """
        info["R"] = sum(self.trace.defender_rewards)
        info["T"] = len(self.trace.defender_actions)
        stop = self.config.L
        for i in range(len(self.trace.defender_actions)):
            if self.trace.defender_actions[i] == 1:
                info[f"stop_{stop}"] = i
                stop -= 1
        return info

    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.state.reset()
        if len(self.trace .attacker_rewards) > 0:
            self.traces.append(self.trace)
        if len(self.traces) > 1 and len(self.traces) % 100 == 0:
            self.__checkpoint_traces()
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        return defender_obs, attacker_obs

    def emulation_evaluation(self, n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy,
                             attacker_policy: Policy,
                             emulation_env_config: EmulationEnvConfig) -> List[EmulationSimulationTrace]:
        traces = []
        for i in range(n_episodes):
            done = False
            s = EmulationEnvState(emulation_env_config=emulation_env_config)
            s.initialize_defender_machines()
            o = self.reset()
            (d_obs, a_obs) = o
            t = 0
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                             initial_defender_observation_state=s.defender_obs_state,
                                             emulation_name=emulation_env_config.name)
            while not done:
                a1 = defender_policy.action(d_obs)
                a2 = attacker_policy.action(a_obs)
                o, r, done, info = self.step((a1,a2))
                (d_obs, a_obs) = o
                r_1, r_2 = r
                if a1 == 0:
                    defender_action = EmulationDefenderStoppingActions.CONTINUE(index=-1)
                else:
                    defender_action = EmulationDefenderStoppingActions.CONTINUE(index=-1)
                if self.state.s == 1:
                    if t >= len(intrusion_seq):
                        t = 0
                    attacker_action = intrusion_seq[t]
                else:
                    attacker_action = EmulationAttackerStoppingActions.CONTINUE(index=-1)
                emulation_trace = Emulator.run_actions(
                    emulation_env_config=emulation_env_config, attacker_action=attacker_action,
                    defender_action=defender_action, trace=emulation_trace,
                    sleep_time=emulation_env_config.log_sink_config.time_step_len_seconds)
            simulation_trace = self.trace
            em_sim_trace = EmulationSimulationTrace(emulation_trace=emulation_trace, simulation_trace=simulation_trace)
            traces.append(em_sim_trace)
        return traces

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
          -human: render to the current display or terminal and return nothing. Usually for human consumption.
          -rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                      representing RGB values for an x-by-y pixel image, suitable
                      for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplemented("Rendering is not implemented for this environment")

    def is_defense_action_legal(self, defense_action_id: int) -> bool:
        """
        Checks whether a defender action in the environment is legal or not

        :param defense_action_id: the id of the action
        :return: True or False
        """
        return True

    def is_attack_action_legal(self, attack_action_id: int) -> bool:
        """
        Checks whether an attacker action in the environment is legal or not

        :param attack_action_id: the id of the attacker action
        :return: True or False
        """
        return True

    def get_traces(self) -> List[SimulationTrace]:
        """
        :return: the list of simulation traces
        """
        return self.traces

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        self.traces = []

    def __checkpoint_traces(self) -> None:
        """
        Checkpoints agent traces
        :return: None
        """
        SimulationTrace.save_traces(traces_save_dir=self.config.save_dir,
                                    traces=self.traces, traces_file="taus.json")
