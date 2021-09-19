import json
import tweepy

from datetime import datetime,date

# PATH="/home/pi/Bots/GoogleFrends/"
PATH = "./"

class WrapperTwitter():

    def __init__(self,debug=False):
        """The constructor."""
        self.__debug = debug
        self.__token = self._get_credentials()
        self.__api   = self._connect()

    def _get_credentials(self):
        """Get the credentials stored in `credentials.json`

        :return: connection token
        :rtype: dict
        """
        with open(f"{PATH}modules/credentials.json", "r") as f:
            token = json.load(f)
        return token

    def _connect(self):
        """Connect to the Twitter API."""
        auth = tweepy.OAuthHandler(
            self.__token["API_KEY"],
            self.__token["API_SECRET_KEY"],
        )
        auth.secure = True
        auth.set_access_token(
            self.__token["ACCESS_TOKEN"],
            self.__token["ACCESS_TOKEN_SECRET"],
        )
        api = tweepy.API(auth,wait_on_rate_limit=True)
        
        if self.__debug:
            print(f"Connected to '{api.me().name}' @{api.me().screen_name}")
        return api

    def postImage(self,status):
        """Post file on Twitter"""
        filename = f"{PATH}assets/output.png" 
        self.__api.update_with_media(filename, status)