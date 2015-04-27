from datetime import datetime
from datetime import timedelta
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
import socket



class BaseListener(object):
    """
    Base class for listeners. Extend and implement listen() to suit
    your acceptance test.
    """
    __metaclass__ = ABCMeta
    def __init__(self, msg='knock-knock'):
        self._msg = msg

    @abstractmethod
    def listen(self, queue, sem):
        """Puts True in queue if it gets message on socket, False otherwise"""
        pass


class TCPListener(BaseListener):
    def __init__(self, host, port, msg='knock-knock', timeout=5):
        BaseListener.__init__(self, msg=msg)
        self._port = port
        self._remote_host_ip = socket.gethostbyname(host)
        self._timeout = 5

    def listen(self, queue, sem):
        print('listening')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', self._port))
            sock.listen(5)
            sock.settimeout(self._timeout)
        except:
            print('failed to set up TCP listener socket')
        finally:
            sem.release()

        start = datetime.now()
        print('before loop')
        try:
            while datetime.now() < start + timedelta(seconds=self._timeout):
                s, (host_ip, host_port) = sock.accept()
                if host_ip == self._remote_host_ip:
                    msg = s.recv(1024)
                    print(msg)
                    queue.put(msg == self._msg)
                    s.close()
                    break
                s.close()
        except:
            queue.put(False)
        sock.close()
        print('done listening')


class UDPListener(BaseListener):
    def __init__(self, port, msg='knock-knock', timeout=5):
        BaseListener.__init__(self, msg=msg)
        self._port = port
        self._timeout = 5

    def listen(self, queue, sem):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', self._port))
            sock.listen(5)
            sock.settimeout(self._timeout)
        except:
            print('failed to set up UDP listener socket')
        finally:
            sem.release()

        start = datetime.now()
        print('listening...')
        try:
            while start + timedelta(seconds=self._timeout) < datetime.now():
                msg = sock.recv(1024)
                if msg == self._msg:
                    print('Listener: %s' % (msg))
                    queue.put(True)
                    break
        except:
            queue.put(False)
        sock.close()
        print('done listening')
