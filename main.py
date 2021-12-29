from datetime import datetime

from twitter.tweepy_wrapper import TweepyWrapper
from twitter.tweet_creator import TweetCreator


def main(datetime: datetime):
    tweepy_wrapper = TweepyWrapper()

    # Create status and media to post on Twitter
    status = TweetCreator.create_status(date=datetime)
    media = TweetCreator.create_media()

    # Post status and media on Twitter
    tweepy_wrapper.post_media(
        status=status,
        filename=datetime.strftime("%Y.%m.%d-%H"),
        file=media,
    )


if __name__ == "__main__":
    datetime = datetime.now()
    try:
        main(datetime=datetime)
        print(f"{datetime.strftime('%Y-%m-%d %H:%M:%S')}: Success")
    except Exception as error:  # TODO define what to except
        print(f"{datetime.strftime('%Y-%m-%d %H:%M:%S')}: Fail, {error}")
