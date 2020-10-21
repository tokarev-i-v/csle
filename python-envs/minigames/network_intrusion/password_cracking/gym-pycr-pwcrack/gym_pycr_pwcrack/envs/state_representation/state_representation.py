from typing import Tuple
import numpy as np
import gym
from gym_pycr_pwcrack.dao.observation.observation_state import ObservationState

class StateRepresentation:
    """
    Utility class for configuring state and observation representations for the pycr-pwcrack env
    """

    @staticmethod
    def base_representation_spaces(obs_state: ObservationState)-> Tuple:
        """
        Configures observation spaces for the base representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_m_features = 10 + obs_state.num_ports + obs_state.num_vuln
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        network_orig_shape = (obs_state.num_machines, num_m_features)
        machine_orig_shape = (num_m_features,)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(num_m_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def base_representation(num_machines : int, num_ports : int, obs_state :ObservationState,
                            vuln_lookup: dict, service_lookup: dict, os_lookup: dict) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Base observation representation, includes all available information. E.g. for each machine: ports, ip, os,
        vulnerabilities, services, cvss, shell, root, flags, etc.

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :param vuln_lookup: lookup dict for converting categorical vuln into numerical
        :param service_lookup: lookup dict for converting categorical service into numerical
        :param os_lookup: lookup dict for converting categorical os into numerical
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 10 + obs_state.num_ports + obs_state.num_vuln
        machines_obs = np.zeros((num_machines, num_m_features))
        ports_protocols_obs = np.zeros((num_machines, num_ports))
        for i in range(num_machines):

            if len(obs_state.machines) > i:
                machines_obs[i][0] = i + 1
                obs_state.machines[i].sort_ports()
                obs_state.machines[i].sort_cve_vuln(vuln_lookup)
                obs_state.machines[i].sort_shell_access(service_lookup)

                # IP
                host_ip = int(obs_state.machines[i].ip.rsplit(".", 1)[-1])
                machines_obs[i][1] = host_ip

                # OS
                os_id = os_lookup[obs_state.machines[i].os]
                machines_obs[i][2] = os_id

                # Ports
                for j, p in enumerate(obs_state.machines[i].ports):
                    s_id = service_lookup[p.service]
                    if j < obs_state.num_ports:
                        machines_obs[i][j + 3] = s_id
                        ports_protocols_obs[i][j] = p.protocol.value

                # Vulnerabilities
                for j, v in enumerate(obs_state.machines[i].cve_vulns):
                    v_id = vuln_lookup[v.name]
                    if j < obs_state.num_vuln:
                        machines_obs[i][j + 3 + obs_state.num_ports] = v_id

                # Num Open Ports
                machines_obs[i][3 + obs_state.num_ports + obs_state.num_vuln] = len(obs_state.machines[i].ports)

                # Num Vulnerabilities
                machines_obs[i][4 + obs_state.num_ports + obs_state.num_vuln] = len(obs_state.machines[i].cve_vulns)

                # Total CVSS score
                total_cvss = sum(list(map(lambda x: x.cvss, obs_state.machines[i].cve_vulns)))
                machines_obs[i][5 + obs_state.num_ports + obs_state.num_vuln] = total_cvss

                # Shell Access
                machines_obs[i][6 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].shell_access)

                # Logged in
                machines_obs[i][7 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].logged_in)

                # Root access
                machines_obs[i][8 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].root)

                # Flag pts
                flag_pts_score = sum([f.score for f in obs_state.machines[i].flags_found])
                machines_obs[i][9 + obs_state.num_ports + obs_state.num_vuln] = int(flag_pts_score)

                # sh_services
                services = []
                for j, sh_c in enumerate(obs_state.machines[i].shell_access_credentials):
                    if sh_c.service is not None:
                        s_id = service_lookup[sh_c.service]
                        if j < obs_state.num_sh and s_id not in services:
                            services.append(s_id)
                            machines_obs[i][j + 3 + obs_state.num_ports + obs_state.num_vuln] = s_id

        return machines_obs, ports_protocols_obs

    @staticmethod
    def compact_representation_spaces(obs_state: ObservationState) -> Tuple:
        """
        Configures observation spaces for the base representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_m_features = 8
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        network_orig_shape = (obs_state.num_machines, num_m_features)
        machine_orig_shape = (num_m_features,)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(num_m_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def compact_representation(num_machines: int, num_ports: int, obs_state: ObservationState) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Compact observation representation, includes only aggregate features, e.g. total num open ports rather than
        a list of all ports

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 8
        machines_obs = np.zeros((num_machines, num_m_features))
        ports_protocols_obs = np.zeros((num_machines, num_ports))
        for i in range(num_machines):
            if len(obs_state.machines) > i:
                machines_obs[i][0] = 1 # machine found

                # Shell Access
                machines_obs[i][1] = int(obs_state.machines[i].shell_access)

                # Logged in
                machines_obs[i][2] = int(obs_state.machines[i].logged_in)

                # Filesystem searched
                machines_obs[i][3] = int(obs_state.machines[i].filesystem_searched)

                # Untried credentials
                machines_obs[i][4] = int(obs_state.machines[i].untried_credentials)

                # SSH brute tried
                machines_obs[i][5] = int(obs_state.machines[i].untried_credentials)

                # Telnet brute tried
                machines_obs[i][6] = int(obs_state.machines[i].untried_credentials)

                # FTP brute tried
                machines_obs[i][7] = int(obs_state.machines[i].untried_credentials)

        return machines_obs, ports_protocols_obs