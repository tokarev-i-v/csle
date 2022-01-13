from typing import Set


class NodeFirewallConfig:
    """
    A DTO object representing a firewall configuration of a container in an emulation environment
    """

    def __init__(self, ip: str, hostname: str, default_gw: str, output_accept: Set[str], input_accept: Set[str],
                 forward_accept: Set[str], output_drop: Set[str], input_drop: Set[str],
                 forward_drop: Set[str], default_output, default_input, default_forward,
                 routes: Set[str]
                 ):
        """
        Intializes the DTO

        :param ip: the ip of the node
        :param hostname: the hostname of the node
        :param default_gw: the default gw
        :param output_accept: the list of ips to accept output
        :param input_accept: the list of ips to accept input
        :param forward_accept: the list of ips to accept forward
        :param output_drop: the list of ips to drop output
        :param input_drop: the list of ips to drop input
        :param forward_drop: the list of ips to drop forward
        :param default_output: the default output
        :param default_input: the default input
        :param default_forward: the default forward
        :param routes: the set of custom routes for the routing table
        """
        self.ip = ip
        self.hostname = hostname
        self.default_gw = default_gw
        self.output_accept = output_accept
        self.input_accept = input_accept
        self.forward_accept = forward_accept
        self.output_drop = output_drop
        self.input_drop = input_drop
        self.forward_drop = forward_drop
        self.default_output = default_output
        self.default_input = default_input
        self.default_forward = default_forward
        self.routes = routes

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, default_gw:{self.default_gw}, output_accept:{self.output_accept}, " \
               f"input_accept:{self.input_accept}, forward_accept:{self.forward_accept}, " \
               f"output_drop:{self.output_drop}, " \
               f"input_drop:{self.input_drop}, forward_drop:{self.forward_drop}, default_output:{self.default_output}, " \
               f"default_input:{self.default_input}, default_forward:{self.default_forward}, " \
               f"routers:{self.routes}, hostname: {self.hostname}"