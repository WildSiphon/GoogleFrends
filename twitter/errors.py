class TweepyWrapperError(Exception):
    pass


class TwitterTokenError(TweepyWrapperError):
    pass


class TwitterConnectionError(TweepyWrapperError):
    pass
