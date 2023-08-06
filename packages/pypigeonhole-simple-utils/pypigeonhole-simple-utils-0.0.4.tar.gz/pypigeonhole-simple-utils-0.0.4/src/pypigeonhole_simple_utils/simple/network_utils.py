import enum


class RemoteServer:
    def __init__(self, host: str, port: int = None):  # if port is None, assume default port
        self.host = host
        self.port = port

    def address(self):
        if self.port:
            return '{}:{}'.format(self.host, self.port)
        else:
            return self.host

    def __str__(self):
        return self.address()


class ProxyType(enum.Enum):
    HTTP = 'http'
    SOCKS4 = 'socks4'
    SOCKS5 = 'socks5'


class ProxyServer(RemoteServer):
    def __init__(self, host: str, port: int = None, proxy_type: ProxyType = ProxyType.HTTP):
        RemoteServer.__init__(self, host, port)
        self.proxy_type = proxy_type


class Credential:
    def __init__(self, user, password: str = None, ssh_key_file: str = None):
        self.user = user
        self.password = password
        self.ssh_key_file = ssh_key_file

    def __repr__(self):
        return 'Credential{{user={}, password={}, ssh_key_file={}}}'.format(self.user, '********', self.ssh_key_file)
