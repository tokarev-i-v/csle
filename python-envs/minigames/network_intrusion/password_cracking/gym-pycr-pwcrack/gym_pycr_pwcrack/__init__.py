"""
Register OpenAI Envs
"""
from gym.envs.registration import register

# -------- Difficulty Level: Simple, Mode: Simulation, Version: Base ------------
register(
    id='pycr-pwcrack-simple-sim-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleSimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-simple-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-simple-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-simple-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-simple-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-simple-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-simple-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Simple, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-simple-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackSimpleCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Simulation, Version: Base ------------
register(
    id='pycr-pwcrack-medium-sim-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumSimBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-medium-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-medium-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-medium-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-medium-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-medium-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Generated Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-medium-generated-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumGeneratedSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Simulation, Version: 1 ------------
register(
    id='pycr-pwcrack-medium-sim-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackMediumSim1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Intermediate, Mode: Cluster, Version: Base ------------
register(
    id='pycr-pwcrack-intermediate-cluster-base-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackIntermediateClusterBaseEnv',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Intermediate, Mode: Cluster, Version: 1 ------------
register(
    id='pycr-pwcrack-intermediate-cluster-v1',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackIntermediateCluster1Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 2 ------------
register(
    id='pycr-pwcrack-intermediate-cluster-v2',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackIntermediateCluster2Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 3 ------------
register(
    id='pycr-pwcrack-intermediate-cluster-v3',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackIntermediateCluster3Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)

# -------- Difficulty Level: Medium, Mode: Cluster, Version: 4 ------------
register(
    id='pycr-pwcrack-intermediate-cluster-v4',
    entry_point='gym_pycr_pwcrack.envs.pycr_pwcrack_env:PyCRPwCrackIntermediateCluster4Env',
    kwargs={'env_config': None, 'cluster_config': None, "checkpoint_dir": None}
)