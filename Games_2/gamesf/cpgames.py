
import warnings
if __name__ == '__main__':
    from core import *
else:
    from .core import *
warnings.filterwarnings('ignore')

class CPGames():
    def __init__(self):
        self.supported_games = {
            'wastesorting': WasteSortinggame,    
        }
    def execute(self, config={}):
        client = self.supported_games["wastesorting"](**config)
        client.run()
if __name__ == '__main__':
    games_client = CPGames()
    games_client.execute()
