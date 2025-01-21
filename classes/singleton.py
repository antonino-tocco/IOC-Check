import threading

class Singleton(type):
    __instances =  {}
    __lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


def singleton(cls):
    __instances = {}
    __lock = threading.Lock()
    def wrapper(*args, **kwargs):
        with __lock:
            if cls not in __instances:
                __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]
    return wrapper