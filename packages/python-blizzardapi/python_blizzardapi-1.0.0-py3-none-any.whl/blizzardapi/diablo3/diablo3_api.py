from .diablo3_game_data_api import Diablo3GameDataApi


class Diablo3Api:
    def __init__(self, client_id, client_secret):
        self.game_data = Diablo3GameDataApi(client_id, client_secret)
