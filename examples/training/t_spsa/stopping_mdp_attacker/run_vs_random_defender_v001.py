import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.policy_type import PolicyType

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-003")
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-mdp-attacker-002")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}tspsa_test",
        title="T-SPSA training attacker to learn 2L thresholds",
        random_seeds=[399, 98912], agent_type=AgentType.T_SPSA,
        log_every=10,
        hparams={
            constants.T_SPSA.N: HParam(
                value=200, name=constants.T_SPSA.N,
                descr="the number of training iterations"),
            constants.T_SPSA.c: HParam(
                value=10, name=constants.T_SPSA.c,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            constants.T_SPSA.a: HParam(
                value=1, name=constants.T_SPSA.a,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.A: HParam(
                value=100, name=constants.T_SPSA.A,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.LAMBDA: HParam(
                value=0.602, name=constants.T_SPSA.LAMBDA,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            constants.T_SPSA.EPSILON: HParam(
                value=0.101, name=constants.T_SPSA.EPSILON,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            constants.T_SPSA.L: HParam(value=3, name=constants.T_SPSA.L,
                                       descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            constants.T_SPSA.THETA1: HParam(value=[-4] * (3 * 2), name=constants.T_SPSA.THETA1,
                                            descr="initial thresholds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=constants.T_SPSA.GRADIENT_BATCH_SIZE,
                descr="the batch size of the gradient estimator"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            constants.T_SPSA.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=constants.T_SPSA.POLICY_TYPE,
                descr="policy type in T-SPSA")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )
    simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
        player_type=PlayerType.DEFENDER, stage_policy_tensor=None)
    agent = TSPSAAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
