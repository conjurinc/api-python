from functools import wraps
from os import unsetenv


def unset_env_var(env_var):
    """
    Unsets an environment variable before calling wrapped function
    :param env_var: Name of environment variable to unset
    :return: Result of wrapped function
    """
    def inner(f):
        @wraps
        def wrapped(*args, **kwargs):
            unsetenv(env_var)
            return f(*args, **kwargs)
        return wrapped
    return inner
