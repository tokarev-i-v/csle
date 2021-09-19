from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_base import PyCrCTFLevel1Base
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_v1 import PyCrCTFLevel1V1
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_v2 import PyCrCTFLevel1V2
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_v3 import PyCrCTFLevel1V3
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_v4 import PyCrCTFLevel1V4
from gym_pycr_ctf.envs_model.config.level_1.pycr_ctf_level_1_nocache_v1 import PyCrCTFLevel1NoCacheV1

# -------- Base Version ------------

class PyCRCTFLevel1EmulationBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1Base.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1Base.env_config(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(PyCRCTFLevel1EmulationBaseEnv, self).__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRCTFLevel1Emulation1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V1.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V1.defender_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                               subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V1.env_config(network_conf=network_conf, attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 No Cache ------------

class PyCRCTFLevel1EmulationNoCache1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    No cache
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1NoCacheV1.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                       subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                       hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1NoCacheV1.defender_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                               subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1NoCacheV1.env_config(network_conf=network_conf,
                                                           attacker_action_conf=attacker_action_conf,
                                                           defender_action_conf=defender_action_conf,
                                                           emulation_config=emulation_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 With costs ------------

class PyCRCTFLevel1EmulationWithCosts1Env(PyCRCTFEnv):
    """
    Uses a minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V1.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V1.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRCTFLevel1Emulation2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V2.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with Costs ------------

class PyCRCTFLevel1EmulationWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V2.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip()),
            defender_action_conf = PyCrCTFLevel1V2.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel1Emulation3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V3.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with Costs ------------

class PyCRCTFLevel1EmulationWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V3.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V3.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel1Emulation4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V4.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs ------------

class PyCRCTFLevel1EmulationWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel1Base.render_conf()
            if emulation_config is None:
                emulation_config = PyCrCTFLevel1Base.emulation_config()
            network_conf = PyCrCTFLevel1Base.network_conf()
            attacker_action_conf = PyCrCTFLevel1V4.attacker_actions_conf(num_nodes=PyCrCTFLevel1Base.num_nodes(),
                                                                         subnet_mask=PyCrCTFLevel1Base.subnet_mask(),
                                                                         hacker_ip=PyCrCTFLevel1Base.hacker_ip())
            defender_action_conf = PyCrCTFLevel1V4.defender_actions_conf(
                num_nodes=PyCrCTFLevel1Base.num_nodes(), subnet_mask=PyCrCTFLevel1Base.subnet_mask())
            env_config = PyCrCTFLevel1V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)