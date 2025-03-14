from src.core.logging_decorator import log_method


def singleton(cls):
    """
    Decorator that transforms a class into a singleton.
    Preserves inheritance and allows the class to be a subclass of other classes.
    """
    instances = {}

    @log_method
    def get_instance(*args, **kwargs):
        """
        Returns the instance of the singleton class.
        :param args:
        :param kwargs:
        :return:
        """
        try:
            instance = instances[cls]
            if args or kwargs:
                try:
                    instance.configure(*args, **kwargs)
                except AttributeError:
                    pass
        except KeyError:
            instance = cls(*args, **kwargs)
            instances[cls] = instance

        return instance

    @log_method
    def reset_instance():
        """
        Resets the instance of the singleton class.
        """
        try:
            del instances[cls]
        except KeyError:
            pass

    # Make get_instance look like the original class
    get_instance.__name__ = cls.__name__
    get_instance.__doc__ = cls.__doc__
    get_instance.reset_instance = reset_instance

    return get_instance
