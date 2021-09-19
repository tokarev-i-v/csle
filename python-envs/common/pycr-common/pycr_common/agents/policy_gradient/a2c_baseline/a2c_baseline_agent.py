"""
An agent for the PyCr env that uses the A2C Policy Gradient algorithm from OpenAI stable baselines
"""
import time
import math

from pycr_common.rendering.video.pycr_ctf_monitor import PyCrCTFMonitor
from pycr_common.dao.envs.base_pycr_env import BasePyCREnv
from pycr_common.dao.experiment.base_experiment_result import BaseExperimentResult
from pycr_common.agents.train_agent import TrainAgent
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.agents.policy_gradient.a2c_baseline.impl.a2c import A2C
from pycr_common.agents.util.agent_util import AgentUtil


class A2CBaselineAgent(TrainAgent):
    """
    An agent for the PyCr env that uses the A2C Policy Gradient algorithm from OpenAI stable baselines
    """

    def __init__(self, env: BasePyCREnv, attacker_config: AgentConfig, eval_env: BasePyCREnv):
        """
        Initialize environment and hyperparameters

        :param attacker_config: the attacker configuration
        """
        super(A2CBaselineAgent, self).__init__(env, attacker_config, eval_env)

    def train(self) -> BaseExperimentResult:
        """
        Starts the training loop and returns the result when complete

        :return: the training result
        """

        # Custom MLP policy
        net_arch = []
        pi_arch = []
        vf_arch = []
        for l in range(self.attacker_config.shared_layers):
            net_arch.append(self.attacker_config.shared_hidden_dim)
        for l in range(self.attacker_config.pi_hidden_layers):
            pi_arch.append(self.attacker_config.pi_hidden_dim)
        for l in range(self.attacker_config.vf_hidden_layers):
            vf_arch.append(self.attacker_config.vf_hidden_dim)


        net_dict = {"pi":pi_arch, "vf":vf_arch}
        net_arch.append(net_dict)

        policy_kwargs = dict(activation_fn=AgentUtil.get_hidden_activation(config=self.attacker_config), net_arch=net_arch)
        device = "cpu" if not self.attacker_config.gpu else "cuda:" + str(self.attacker_config.gpu_id)
        policy = "MlpPolicy"

        if self.attacker_config.lr_progress_decay:
            temp = self.attacker_config.alpha
            lr_decay_func = lambda x: temp*math.pow(x, self.attacker_config.lr_progress_power_decay)
            self.attacker_config.alpha = lr_decay_func

        model = A2C(policy, self.env,
                    learning_rate=self.attacker_config.alpha,
                    n_steps=self.attacker_config.batch_size,
                    gamma=self.attacker_config.gamma,
                    gae_lambda=self.attacker_config.gae_lambda,
                    max_grad_norm=self.attacker_config.max_gradient_norm,
                    verbose=1,
                    seed=self.attacker_config.random_seed,
                    policy_kwargs=policy_kwargs,
                    device=device,
                    agent_config=self.attacker_config,
                    vf_coef=self.attacker_config.vf_coef,
                    ent_coef=self.attacker_config.ent_coef,
                    env_2=self.eval_env
                    )

        if self.attacker_config.load_path is not None:
            A2C.load(self.attacker_config.load_path, policy, agent_config=self.attacker_config)


        # Eval config
        if self.attacker_config.video or self.attacker_config.gifs:
            time_str = str(time.time())
            if self.attacker_config.video_dir is None:
                raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                     "the video_dir argument")
            train_eval_env = PyCrCTFMonitor(self.env, self.attacker_config.video_dir + "/" + time_str, force=True,
                                      video_frequency=self.attacker_config.video_frequency, openai_baseline=True)
            train_eval_env.metadata["video.frames_per_second"] = self.attacker_config.video_fps

        eval_env = None

        if self.eval_env is not None:
            eval_env = PyCrCTFMonitor(self.eval_env, self.attacker_config.video_dir + "/" + time_str, force=True,
                                          video_frequency=self.attacker_config.video_frequency, openai_baseline=True)
            eval_env.metadata["video.frames_per_second"] = self.attacker_config.video_fps

        model.learn(total_timesteps=self.attacker_config.num_episodes,
                    log_interval=self.attacker_config.train_log_frequency,
                    eval_freq=self.attacker_config.eval_frequency,
                    n_eval_episodes=self.attacker_config.eval_episodes,
                    eval_env=train_eval_env,
                    eval_env_2=eval_env
                    )

        self.attacker_config.logger.info("Training Complete")

        # Save networks
        model.save_model()

        # Save other game data
        if self.attacker_config.save_dir is not None:
            time_str = str(time.time())
            model.train_result.to_csv(self.attacker_config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
            model.eval_result.to_csv(self.attacker_config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

        self.train_result = model.train_result
        self.eval_result = model.eval_result
        return model.train_result


    def get_action(self, s, eval=False, attacker=True) -> int:
        raise NotImplemented("not implemented")

    def eval(self, log=True) -> BaseExperimentResult:
        raise NotImplemented("not implemented")