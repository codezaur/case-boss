from functools import wraps


def validate_is_dict(func):
    @wraps(func)
    def wrapper(self, source, *args, **kwargs):
        if not isinstance(source, dict):
            raise TypeError(
                f"{func.__name__} expects dict, got {type(source).__name__}"
            )
        return func(self, source, *args, **kwargs)

    return wrapper
