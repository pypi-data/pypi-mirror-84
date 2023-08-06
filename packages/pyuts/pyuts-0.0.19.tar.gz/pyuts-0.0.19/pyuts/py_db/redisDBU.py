from ..py_api_b import PyApiB
from ..py_file.fileU import FileU
from ..py_mix.envU import EnvU
import redis


class RedisDBU(PyApiB):
    """
    Redis数据库工具
    """
    HOST_KEY = "redis_host"
    PORT_KEY = "redis_port"
    USER_KEY = "redis_user"
    PSWD_KEY = "redis_pswd"
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.initByEnvFile()
        self.initByEnv()
        
    def initByEnv(self):
        _envU = EnvU()
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _port = _envU.get(self.PSWD_KEY)
            self.init(_host,_port,_user,_port)
        
    def initByEnvFile(self, env_path='./dockers/.env'):
        _envU = FileU.produce().read_env(env_path)
        _host = _envU.get(self.HOST_KEY)
        if _host:
            _port = int(_envU.get(self.PORT_KEY,"1"))
            _user = _envU.get(self.USER_KEY)
            _port = _envU.get(self.PSWD_KEY)
            self.init(_host,_port,_user,_port)

    def init(self, host=None, port=None, user=None, pswd=None):
        self.r:redis.Redis = redis.Redis(host=host, port=port, decode_responses=True, password=pswd)
        self.r.pipeline()
    
    