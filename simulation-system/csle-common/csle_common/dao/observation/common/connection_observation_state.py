
class ConnectionObservationState:
    """
    A DTO representing a connection observation DTO
    """

    def __init__(self, conn, username : str, root: bool, service: str, port: int, tunnel_thread = None,
                 tunnel_port : int = None, interactive_shell = None, proxy = None, ip = None):
        """
        Intializes the DTO

        :param conn: the connection object
        :param username: the username of the connection
        :param root: whether the connection is root or not
        :param service: the service of the connection
        :param port: the port of the connection
        :param tunnel_thread: the tunnel thread for the connection
        :param tunnel_port: the tunnel port of the connection
        :param interactive_shell: an interactive shell of the connection
        :param proxy: a proxy for the connection
        :param ip: the ip of the connection
        """
        self.conn = conn
        self.username = username
        self.root = root
        self.port = port
        self.service = service
        self.tunnel_thread = tunnel_thread
        self.tunnel_port = tunnel_port
        self.interactive_shell = interactive_shell
        self.proxy = proxy
        self.ip = ip

    def __str__(self) -> str:
        """
        :return: a string representation of the connection observation
        """
        return "username:{},root:{},service:{},port:{}".format(self.username, self.root, self.service, self.port)

    def __eq__(self, other) -> bool:
        """
        Checks for equality with another connection

        :param other: the other connection to compare with
        :return: True if equal, otherwise False
        """
        if not isinstance(other, ConnectionObservationState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.username == other.username and self.root == other.root and self.service == other.service \
               and self.port == other.port and self.ip == other.ip

    def __hash__(self):
        """
        :return: a hash representation of the object
        """
        return hash(self.username) + 31 * hash(self.root) + 31 * hash(self.service) + 31 * hash(self.port) \
               + 31 * hash(self.ip)

    def cleanup(self) -> None:
        """
        Utility function for cleaning up the connection.

        :return: None
        """

        if self.tunnel_thread is not None:
            try:
                self.tunnel_thread.shutdown()
            except Exception:
                pass
            self.tunnel_thread = None
        if self.interactive_shell is not None:
            try:
                self.interactive_shell.close()
            except Exception:
                pass
            self.interactive_shell = None
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
        if self.proxy is not None:
            try:
                self.proxy.cleanup()
            except Exception:
                pass
            self.proxy = None