from typing import List
from scipy.stats import betabinom
import numpy as np
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig


class IntrusionRecoveryPomdpUtil:
    """
    Class with utility functions for the intrusion-recovery POMDP
    """

    @staticmethod
    def state_space() -> List[int]:
        """
        Gets the state space of the POMDP

        :return: a list with the states
        """
        return [0, 1, 2]

    @staticmethod
    def initial_belief(p_a: float) -> List[float]:
        """
        Gets the initial belief state of the POMDP

        :param p_a: the attack probability
        :return: the initial belief state
        """
        return [1 - p_a, p_a, 0]

    @staticmethod
    def action_space() -> List[int]:
        """
        Gets the action space of the POMDP

        :return: a list with the actions
        """
        return [0, 1]

    @staticmethod
    def observation_space(num_observations: int) -> List[int]:
        """
        Gets the observation space of the POMDP

        :param num_observations: the number of observations
        :return: a list with the actions
        """
        return list(range(num_observations))

    @staticmethod
    def cost_function(s: int, a: int, eta: float, negate: bool = False) -> float:
        """
        Cost function of the POMDP

        :param s: the state
        :param a: the action
        :param eta: the scaling factor
        :param negate: boolean flag, if true then return negated version of the cost (the reward)
        :return: the cost or reward
        """
        if s == 2:
            return 0
        cost = eta * s - eta * a * s + a
        if negate:
            return -cost
        else:
            return cost

    @staticmethod
    def cost_tensor(eta: float, states: List[int], actions: List[int], negate: bool = False) -> List[List[float]]:
        """
        Creates a |A|x|S| tensor with the costs (or rewards) of the POMDP

        :param eta: the cost scaling factor
        :param states: the list of states
        :param actions: the list of actions
        :param negate: a boolean flag indicating whether the cost should be negated as a reward or not
        :return: A tensor with the costs (or rewards)
        """
        cost_tensor = []
        for a in actions:
            a_costs = []
            for s in states:
                a_costs.append(IntrusionRecoveryPomdpUtil.cost_function(s=s, a=a, eta=eta, negate=negate))
            cost_tensor.append(a_costs)
        return cost_tensor

    @staticmethod
    def observation_function(s: int, o: int, num_observations: int) -> float:
        """
        The observation function of the POMDP

        :param s: the state
        :param o: the observation
        :param num_observations: the total number of observations
        :return: the probability P(o | s)
        """
        if s == 0:
            no_intrusion_rv = betabinom(n=num_observations - 1, a=0.7, b=3)
            return float(no_intrusion_rv.pmf(o))
        elif s == 1:
            intrusion_rv = betabinom(n=num_observations - 1, a=1, b=0.7)
            return float(intrusion_rv.pmf(o))
        else:
            if o == num_observations - 1:
                return 1.0
            else:
                return 0.0

    @staticmethod
    def observation_tensor(states: List[int], observations: List[int]) -> List[List[float]]:
        """
        Creates a |S|x|O| tensor with the observation probabilities

        :param states: the list of states
        :param observations: the list of observations
        :return: the observation tensor
        """
        observation_tensor = []
        num_observations = len(observations)
        for s in states:
            s_observations = []
            for o in observations:
                s_observations.append(IntrusionRecoveryPomdpUtil.observation_function(
                    s=s, o=o, num_observations=num_observations))
            observation_tensor.append(s_observations)
        return observation_tensor

    @staticmethod
    def transition_function(s: int, s_prime: int, a: int, p_a: float, p_c_1: float, p_u: float, p_c_2: float) -> float:
        """
        The transition function of the POMDP

        :param s: the state
        :param s_prime: the next state
        :param a: the action
        :param p_a: the intrusion probability
        :param p_c_1: the crash probability in the healthy state
        :param p_c_2: the crash probability in the compromised state
        :param p_u: the upgrade probability
        :return: P(s_prime | s, a)
        """
        if s == 2 and s_prime == 2:
            return 1.0
        elif s_prime == 2 and s == 0:
            return p_c_1
        elif s_prime == 2 and s == 1:
            return p_c_2
        elif s_prime == 0 and a == 1 and s == 0:
            return (1.0 - p_a) * (1.0 - p_c_1)
        elif s_prime == 0 and a == 1 and s == 1:
            return (1.0 - p_a) * (1.0 - p_c_2)
        elif s_prime == 1 and a == 1 and s == 0:
            return p_a * (1.0 - p_c_1)
        elif s_prime == 1 and a == 1 and s == 1:
            return p_a * (1.0 - p_c_2)
        elif s_prime == 0 and s == 1 and a == 0:
            return (1.0 - p_c_2) * p_u
        elif s_prime == 0 and s == 0 and a == 0:
            return (1.0 - p_c_1) * (1.0 - p_a)
        elif s_prime == 1 and s == 0 and a == 0:
            return (1.0 - p_c_1) * p_a
        elif s_prime == 1 and s == 1 and a == 0:
            return (1 - p_c_2) * (1 - p_u)
        else:
            return 0

    @staticmethod
    def transition_tensor(states: List[int], actions: List[int], p_a: float, p_c_1: float, p_c_2: float, p_u: float) \
            -> List[List[List[float]]]:
        """
        Creates a |A|x|S|x|S| tensor with the transition probabilities of the POMDP

        :param states: the list of states
        :param actions: the list of actions
        :param p_a: the intrusion probability
        :param p_c_1: the crash probability in the healthy state
        :param p_c_2: the crash probability in the compromised state
        :param p_u: the upgrade probability
        :return: the transition tensor
        """
        transition_tensor = []
        for a in actions:
            a_transitions = []
            for s in states:
                s_a_transitions = []
                for s_prime in states:
                    s_a_transitions.append(IntrusionRecoveryPomdpUtil.transition_function(
                        s=s, s_prime=s_prime, a=a, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u))
                a_transitions.append(s_a_transitions)
            transition_tensor.append(a_transitions)
        return transition_tensor

    @staticmethod
    def sample_initial_state(b1: List[float]) -> int:
        """
        Samples the initial state

        :param b1: the initial belief
        :return: the initial state
        """
        return int(np.random.choice(np.arange(0, len(b1)), p=b1))

    @staticmethod
    def sample_next_observation(observation_tensor: List[List[float]], s_prime: int, observations: List[int]) -> int:
        """
        Samples the next observation

        :param s_prime: the new state
        :param observations: the observation space
        :param observation_tensor: the observation tensor
        :return: the next observation o
        """
        observation_probs = []
        for o in observations:
            observation_probs.append(observation_tensor[s_prime][o])
        o = np.random.choice(np.arange(0, len(observations)), p=observation_probs)
        return int(o)

    @staticmethod
    def bayes_filter(s_prime: int, o: int, a: int, b: List[float], states: List[int], observations: List[int],
                     observation_tensor: List[List[float]], transition_tensor: List[List[List[float]]]) -> float:
        """
        A Bayesian filter to compute b[s_prime] of the POMDP

        :param s_prime: the state to compute the belief for
        :param o: the latest observation
        :param a: the latest action
        :param b: the current belief
        :param states: the list of states
        :param observations: the list of observations
        :param observation_tensor: the observation tensor
        :param transition_tensor: the transition tensor of the POMDP
        :return: b[s_prime]
        """
        norm = 0.0
        for s in states:
            for s_prime_1 in states:
                prob_1 = observation_tensor[s_prime_1][o]
                norm += b[s] * prob_1 * transition_tensor[a][s][s_prime_1]
        if norm == 0.0:
            return 0.0
        temp = 0.0

        for s in states:
            temp += observation_tensor[s_prime][o] * transition_tensor[a][s][s_prime] * b[s]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a}, s_prime:{s_prime}")
        assert round(b_prime_s_prime, 2) <= 1
        if s_prime == 2 and o != observations[-1]:
            assert round(b_prime_s_prime, 2) <= 0.01
        return b_prime_s_prime

    @staticmethod
    def p_o_given_b_a1_a2(o: int, b: List[float], a: int, states: List[int],
                          transition_tensor: List[List[List[float]]], observation_tensor: List[List[float]]) -> float:
        """
        Computes P[o|a,b] of the POMDP

        :param o: the observation
        :param b: the belief point
        :param a: the action
        :param states: the list of states
        :param transition_tensor: the transition tensor
        :param observation_tensor: the observation tensor
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0.0
        for s in states:
            for s_prime in states:
                prob += b[s] * transition_tensor[a][s][s_prime] * observation_tensor[s_prime][o]
        assert prob < 1
        return prob

    @staticmethod
    def next_belief(o: int, a: int, b: List[float], states: List[int], observations: List[int],
                    observation_tensor: List[List[float]], transition_tensor: List[List[List[float]]]) -> List[float]:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a: the latest action of player 1
        :param b: the current belief
        :param states: the list of states
        :param observations: the list of observations
        :param observation_tensor: the observation tensor
        :param transition_tensor: the transition tensor
        :return: the new belief
        """
        b_prime = [0.0] * len(states)
        for s_prime in states:
            b_prime[s_prime] = IntrusionRecoveryPomdpUtil.bayes_filter(
                s_prime=s_prime, o=o, a=a, b=b, states=states, observations=observations,
                transition_tensor=transition_tensor, observation_tensor=observation_tensor)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a:{a}, b:{b}")
        assert round(sum(b_prime), 2) == 1
        return b_prime

    @staticmethod
    def pomdp_solver_file(config: IntrusionRecoveryPomdpConfig) -> str:
        """
        Gets the POMDP environment specification based on the format at http://www.pomdp.org/code/index.html,
        for the defender's local problem against a static attacker

        :param config: the POMDP config
        :return: the file content as a string
        """
        file_str = ""
        file_str = file_str + f"discount: {config.discount_factor}\n\n"
        file_str = file_str + "values: cost\n\n"
        file_str = file_str + f"states: {len(config.states)}\n\n"
        file_str = file_str + f"actions: {len(config.actions)}\n\n"
        file_str = file_str + f"observations: {len(config.observations)}\n\n"
        initial_belief_str = " ".join(list(map(lambda x: str(x), config.b1)))
        file_str = file_str + f"start: {initial_belief_str}\n\n\n"
        num_transitions = 0
        for s in config.states:
            for a in config.actions:
                probs = []
                for s_prime in range(len(config.states)):
                    num_transitions += 1
                    prob = config.transition_tensor[a][s][s_prime]
                    file_str = file_str + f"T: {a} : {s} : {s_prime} {prob:.80f}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"
        for a in config.actions:
            for s_prime in config.states:
                probs = []
                for o in range(len(config.observations)):
                    prob = config.observation_tensor[s_prime][o]
                    file_str = file_str + f"O : {a} : {s_prime} : {o} {prob:.80f}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"
        for s in config.states:
            for a in config.actions:
                for s_prime in config.states:
                    for o in config.observations:
                        c = config.cost_tensor[a][s]
                        file_str = file_str + f"R: {a} : {s} : {s_prime} : {o} {c:.80f}\n"
        return file_str