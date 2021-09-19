"""
A general bot attack agent for PyCr environments that acts greedily according to a pre-trained policy network
"""
import torch
import traceback
import time
from pycr_common.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from pycr_common.dao.network.base_env_state import BaseEnvState
from pycr_common.dao.envs.base_pycr_env import BasePyCREnv
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.agents.config.agent_config import AgentConfig


class PPOAttackerBotAgent:
    """
    Class implementing an attack policy that acts greedily according to a given policy network
    """

    def __init__(self, pg_config: AgentConfig, env_config: BaseEnvConfig, model_path: str = None,
                 env: BasePyCREnv = None):
        """
        Constructor, initializes the policy

        :param pg_config:  agent config
        :param env_config: environment config
        :param model_path: path to saved model
        :param env: the environment
        """
        self.env_config = env_config
        if model_path is None:
            raise ValueError("Cannot create a PPOAttackerBotAgent without specifying the path to the model")
        self.env = env
        self.agent_config = pg_config
        self.model_path = model_path
        self.device = "cpu" if not self.agent_config.gpu else "cuda:" + str(self.agent_config.gpu_id)
        self.initialize_models()

    def initialize_models(self) -> None:
        """
        Initialize models

        :return: None
        """
        # Initialize models
        self.model = PPO.load(env=self.env, load_path=self.agent_config.load_path, device=self.device,
                              agent_config=self.agent_config)

    def action(self, s: BaseEnvState, agent_state = None) -> int:
        """
        Samples an action from the policy.

        :param s: the environment state
        :return: action_id
        """
        try:
            #actions = list(range(self.agent_config.output_dim))
            # non_legal_actions = list(filter(lambda action: not PyCRCTFEnv.is_action_legal(
            #     action, env_config=self.env_config, env_state=s), actions))
            m_obs, p_obs = s.get_attacker_observation()
            obs_tensor = torch.as_tensor(m_obs.flatten()).to(self.device)            
            actions, values = self.model.predict(observation=obs_tensor, deterministic = True,
                                                 state=obs_tensor, attacker=True)
            time.sleep(2)

            action = actions[0]
        except Exception as e:
            print(str(e))
            traceback.print_exc()

        return action