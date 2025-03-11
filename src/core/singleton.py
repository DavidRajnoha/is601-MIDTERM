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
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        elif args or kwargs:
            # If the singleton exists but constructor args provided, update instance
            if hasattr(instances[cls], 'configure'):
                instances[cls].configure(*args, **kwargs)
        return instances[cls]

    @log_method
    def reset_instance():
        """
        Resets the instance of the singleton class.
        """
        if cls in instances:
            del instances[cls]

    # Make get_instance look like the original class
    get_instance.__name__ = cls.__name__
    get_instance.__doc__ = cls.__doc__
    get_instance.reset_instance = reset_instance

    return get_instance
