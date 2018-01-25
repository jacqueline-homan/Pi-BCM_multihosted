class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    model = None

    def __init__(self, model):
        self.model = model

    def first(self, **kwards):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        try:
            result = self.model.objects.get(**kwards)
        except self.model.DoesNotExist:
            result = None
        return result

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        record = self.model(**kwargs)
        record.save()
        return record

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        model.save()
        return model

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.model)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.model))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        model.save()
        return model

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

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.model.objects.filter(**kwargs)

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.model.objects.get(id=id)

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.model.objects.all()
