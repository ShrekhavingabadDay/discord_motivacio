import os

class Env:
    def __init__(self):
        self.env_file = os.path.join(os.path.dirname(__file__), '.env')
        self.env_dict = self.read_env()

    def read_env(self):
        o = {}

        with open(self.env_file, 'r') as f:
            for line in f.readlines():
                key_value_pair = line.strip().split("=")
                o[key_value_pair[0]] = key_value_pair[1]

        return o

    def get(self,key):
        return self.env_dict[key]

getenv = Env
