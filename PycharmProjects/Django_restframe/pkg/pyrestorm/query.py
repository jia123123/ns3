import copy


class RestQuery(object):
    def __deepcopy__(self, memodict={}):
        return copy.deepcopy(self.params)

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.params.update(kwargs)

    def add_qs(self, **kwargs):
        self.params.update(kwargs)


class RestQueryset(object):
    '''
    Wrapper for 'evaluating' API results. Provides access like a list/queryset.
    The cases where evaluation will occur is:
        1) Iteration
        2) Index Access/Slicing
        3) Length/Counting
    '''
    def __init__(self, model, *args, **kwargs):
        # Compatabilities with Django Queryset
        self._prefetch_related_lookups = True

        # RestQuery object storing query attributes
        self.query = RestQuery(**kwargs.get('query', {}))
        # How many records to we have in the _data cache
        self._count = 0
        # Local cache of API objects
        self._data = []
        # What RestModel does this queryset belong to?
        self.model = model
        # Paginator instance for assisted navigation logic with API
        if hasattr(model._meta, 'paginator_class'):
            self._paginator = model._meta.paginator_class()
        # REST Client for performing API calls
        self.client = self.model.get_client()
        self.url = kwargs.pop('url', self.model.get_base_url())

    # 1) Iteration
    def __iter__(self):
        return iter(self._evaluate())

    # 2) Index Access/Slicing
    def __getitem__(self, value):
        # If we are getting a slice, only get part of the queryset
        if isinstance(value, slice):
            self._evaluate(value.start, value.stop)
        # If it is a single element, fetch just that
        elif isinstance(value, int):
            if hasattr(self, '_paginator'):
                self._data = self._evaluate(value, value + 1)[0]
            else:
                self._data = self._evaluate()[value]

        return self._data

    # 3) Length/Counting
    def __len__(self):
        return len(self._evaluate())

    # Returns an identical copy of self
    def _clone(self):
        # New copy of RestQueryset
        clone = self.__class__(model=self.model, query=copy.deepcopy(self.query), url=self.url)

        # Return to the user
        return clone

    # Assmbemble the querystring params for the API call
    def _get_query_params(self):
        params = {}

        # If pagination is on, include those variables
        if hasattr(self, '_paginator'):
            params.update(self._paginator.as_params())

        # Sanatize the parameters since some Python types don't encode well
        for key, value in self.query.params.items():
            if isinstance(value, (set, frozenset)):
                value = list(value)
            params[key] = value
        params.update(params)

        return params

    # Unpaginated API results, only stale once
    def _fetch(self):
        # Retrieve data from the server
        response = self.client.get(self.url, **self._get_query_params())
        self._data = [self.model(_json=item) for item in response]
        self._count = len(self._data)
        return self._data

    def _fetch_pages(self, start, end):
        # Move the paginator to the beginning of the segment of interest
        self._paginator.cursor(start)

        # Naive data reset, we can only cache for the current query
        self._data = []
        self._count = 0

        # While we don't have all the data we need, fetch
        self._paginator.cursor(start, limit=(end if end is None else (end - start)))
        fetch = True
        while fetch:
            # Retrieve data from the server
            response = self.client.get(self.url, **self._get_query_params())

            # Attempt to grab the size of the dataset from the usual place
            self._paginator.set_max(response)

            # Count how many record were retrieved in this round
            count = len(response['results'])

            # Extend the dataset with the new records
            self._data.extend([self.model(_json=item) for item in response['results']])

            # Increment the number of records we currently have in the queryset
            self._count += count

            # Determine if we need to grab another round of records
            fetch = self._paginator.next() if end is None else self._count < (end - start)

        return self._data

    # Performs 'evaluation' by querying the API and bind the results into an array
    def _evaluate(self, start=0, end=None):
        # Using paginated results
        if hasattr(self, '_paginator'):
            end = self._paginator.max if end is None else end
            # Check for valid usage
            if end is not None and start > end:
                raise ValueError('`start` cannot be greater than `end`')
            elif self._paginator.max is not None and end > self._paginator.max:
                # Turns out Python returns the entire list in the event of an 'over slice'
                # where the bounds of the slice extend beyond the length of the list.
                # raise ValueError('`end` cannot be greater than to the maximum number of records')
                pass

            return self._fetch_pages(start, end)

        # Returns unpaginated results
        return self._fetch()

    ''' Public API Contract '''
    # Returns the number of elements to expect from a given query
    def count(self):
        # We don't want to permenantly affect this instance
        clone = self._clone()
        clone._evaluate(end=0)

        return clone._paginator.max

    # Creates a single element, throws and exeception if there is a validation error
    def create(self, **kwargs):
        instance = self.model()

        # Assign all of the attributes to the model
        for key, value in kwargs.items():
            setattr(instance, key, value)

        # Persist to the API
        instance.save()

        return instance

    # Retrieves a single element, throws exceptions if a single element is not found
    def get(self, **kwargs):
        # We don't want to permenantly affect this instance
        clone = self._clone()
        clone.query.add_qs(**kwargs)

        # We only need to know if more than one is returned, extra is only overhead
        results = clone._evaluate()
        count = len(results)
        if count == 0:
            raise self.model.DoesNotExist
        elif count > 1:
            raise self.model.MultipleObjectsReturned

        return results[0]

    # Attempts to retrieve a single element using the kwargs, if the record does not exist it will be created including defaults
    def get_or_create(self, defaults={}, **kwargs):
        created = False
        try:
            instance = self.get(**kwargs)
        except self.model.DoesNotExist:
            defaults.update(kwargs)
            instance = self.create(**defaults)
            created = True

        return (instance, created)

    # Attempts to find multiple items matching query
    def filter(self, **kwargs):
        # We don't want to permenantly affect this instance
        clone = self._clone()
        clone.query.add_qs(**kwargs)

        return clone

    def none(self, *args, **kwargs):
        '''Imitate an empty `RestQueryset` with no results
        '''
        return

    def all(self, *args, **kwargs):
        '''Unmodified query to return all results in the `RestQueryset`
        '''
        return self._clone()
