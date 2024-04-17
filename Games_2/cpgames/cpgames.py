
import warnings
if __name__ == '__main__':
    from core import *
else:
    from .core import *
warnings.filterwarnings('ignore')

class CPGames():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_games = self.initialize()
    def execute(self, config={}):
        client = self.supported_games["catchcoins"](**config)
        client.run()
    def initialize(self):
        supported_games = {
            'catchcoins': CatchCoinsGame,    
        }
        return supported_games

if __name__ == '__main__':
    games_client = CPGames()
    games_client.execute()