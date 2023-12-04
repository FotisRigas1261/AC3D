import os

class PATH:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name=None):
        if not self._initialized:
            self._name = name if name else ""
            self.DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            self.OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", self._name)
            self.TEMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp", self._name)

            self._create_directories()
            self._initialized = True

    def _create_directories(self):
        for path in [self.DATA, self.OUTPUT, self.TEMP]:
            if not os.path.exists(path):
                os.makedirs(path)

    @property
    def name(self):
        return self._name

    @property
    def data_path(self):
        return self.DATA

    @property
    def output_path(self):
        return self.OUTPUT

    @property
    def temp_path(self):
        return self.TEMP