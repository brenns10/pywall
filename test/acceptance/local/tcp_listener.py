from pywall_acceptance_test_case import BaseListener
from datetime import datetime
from datetime import timedelta


class TCPListener(BaseListener):
    def __init__(self, host, port):
        self._port = port
        self._timeout = 5
        self._remote_host_ip = socket.gethostbyname(host)

    def listen(self, queue, sem):
        print('listening')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', self._port))
        sock.listen(5)
        sock.settimeout(self._timeout)
        sem.release()

        start = datetime.now()
        print('before loop')
        try:
            while start + timedelta(seconds=self._timeout) < datetime.now():
                s, (host_ip, host_port) = sock.accept()
                if host_ip == self._remote_host_ip:
                    msg = s.recv(1024)
                    print(msg)
                    queue.put(msg == 'knock-knock')
                    s.close()
                    break
                s.close()
            sock.close()
        except socket.timeout:
            sock.close()
            queue.put(False)
        print('done listening')
