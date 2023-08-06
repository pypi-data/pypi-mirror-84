from .wow_game_data_api import WowGameDataApi
from .wow_profile_api import WowProfileApi


class WowApi:
    def __init__(self, client_id, client_secret):
        self.game_data = WowGameDataApi(client_id, client_secret)
        self.profile = WowProfileApi(client_id, client_secret)
