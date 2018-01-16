class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def __init__(self, model):
        self.__model__ = model

    def first(self, **kwards):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        try:
            result = self.__model__.objects.get(**kwards)
        except self.__model__.DoesNotExist:
            result = None
        return result

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        record = self.__model__(**kwargs)
        record.save()
        return record

    def get_or_create(self, defaults=None, **kwargs):
        """Returns a tuple of service's model class and a boolean indicating
        whether a new, saved instance is created.
        Returns a instance of the service's model with the specified key word arguments or
        returns a new, saved instance of the service's model class.

        :param **kwargs: filter parameters
        """
        row = self.first(**kwargs)
        if row:
            return row, False
        else:
            if defaults is not None:
                kwargs.update(defaults)
            return self.create(**kwargs), True
