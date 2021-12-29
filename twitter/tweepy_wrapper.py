import json
from pathlib import Path

from tweepy import API, OAuthHandler
from tweepy.errors import TweepyException

from twitter.errors import TwitterConnectionError, TwitterTokenError


class TweepyWrapper:
    """
    Homemade wrapper for Tweepy.
    """

    CREDENTIALS_FILEPATH = Path(__file__).parent / "credentials.json"

    TOKEN_REQUIREMENT = {
        "API_KEY",
        "API_SECRET_KEY",
        "ACCESS_TOKEN",
        "ACCESS_TOKEN_SECRET",
    }

    def __init__(self):
        """
        Construct the Tweepy wrapper.
        """
        # Info
        self.info = None

        # Token
        self.token = None
        self.load_token()

        # API
        self.api = None
        self.connect()

    def load_token(self):
        """
        Load and check connection token from JSON file.

        :raises TwitterTokenError: can't load token or token missing parameters
        """
        # Load
        try:
            with open(TweepyWrapper.CREDENTIALS_FILEPATH, "r") as credentials:
                self.token = json.load(credentials)
        except (json.decoder.JSONDecodeError, IOError) as error:
            raise TwitterTokenError(error) from error

        # Check
        if not TweepyWrapper.TOKEN_REQUIREMENT.issubset(self.token):
            missing_parameters = TweepyWrapper.TOKEN_REQUIREMENT - self.token.keys()
            error_message = (
                f"Missing parameter(s) {missing_parameters} "
                f"in '{TweepyWrapper.CREDENTIALS_FILEPATH}'."
            )
            raise TwitterTokenError(error_message)

    def connect(self):
        """
        Connect to the Twitter API.
        """
        auth = OAuthHandler(
            self.token["API_KEY"],
            self.token["API_SECRET_KEY"],
        )
        auth.secure = True
        auth.set_access_token(
            self.token["ACCESS_TOKEN"],
            self.token["ACCESS_TOKEN_SECRET"],
        )
        self.api = API(auth, wait_on_rate_limit=True)

        try:
            self.info = self.api.verify_credentials()._json
        except TweepyException as error:
            error_message = "Failed to establish a new connection to 'api.twitter.com'."
            raise TwitterConnectionError(error_message) from error

    def post_media(self, status, filename, file):
        """
        Post media on Twitter.
        """
        self.api.update_status_with_media(status=status, filename=filename, file=file)
