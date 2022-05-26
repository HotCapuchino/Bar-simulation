from random import randint, triangular

from utils.bar import Bar

class Resources(Bar):
    
    def __init__(self, config) -> None:
        super().__init__()