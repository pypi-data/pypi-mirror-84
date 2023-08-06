import os
import socket
import socks
import paramiko

from pypigeonhole_simple_utils.simple.network_utils import RemoteServer, ProxyType, ProxyServer, Credential
import pypigeonhole_simple_utils.simple.simple_log as dss_log

logger = dss_log.get_logger('__name__')


class FtpClient:
    def __init__(self, ftp_server: RemoteServer, ftp_user: Credential,
                 proxy: ProxyServer = None):
        self._ftp_server = ftp_server
        self._ftp_user = ftp_user
        self._proxy = proxy

    def _socks_proxy_type(self):
        if self._proxy.proxy_type == ProxyType.HTTP:
            return socks.HTTP
        elif self._proxy.proxy_type == ProxyType.SOCKS4:
            return socks.PROXY_TYPE_SOCKS4
        elif self._proxy.proxy_type == ProxyType.SOCKS5:
            return socks.PROXY_TYPE_SOCKS5
        else:
            raise ValueError(f'unknown proxy type: {self._proxy.proxy_type}')

    def download(self, remote_files: list, local_dir: str = '.', overwrite=True) -> list:
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        if self._proxy:
            socks.setdefaultproxy(self._socks_proxy_type(), self._proxy.host, self._proxy.port, True)
        socket.socket = socks.socksocket

        with paramiko.SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self._ftp_user.ssh_key_file:
                ssh_client.connect(self._ftp_server.host, self._ftp_server.port,
                                   self._ftp_user.user, self._ftp_user.password,
                                   key_filename=self._ftp_user.ssh_key_file)
            else:
                ssh_client.connect(self._ftp_server.host, self._ftp_server.port,
                                   self._ftp_user.user, self._ftp_user.password)

            with paramiko.SFTPClient.from_transport(ssh_client.get_transport()) as sftp:
                missing = []
                for idx, file_name in enumerate(remote_files):
                    local_file = os.path.join(local_dir, file_name)
                    if os.path.exists(local_file) and not overwrite:
                        continue

                    try:
                        logger.info('download file:#%s: %s', idx, file_name)
                        sftp.get(file_name, local_file)
                    except FileNotFoundError as e:
                        missing.append(local_file)
                        # sftp creates an empty file with this name, so remove it
                        if os.path.exists(local_file):
                            os.remove(local_file)
                        err_no, err_str = e.args
                        logger.error('File %s download results I/O error(%s): %s', local_file, err_no, err_str)

                return missing
