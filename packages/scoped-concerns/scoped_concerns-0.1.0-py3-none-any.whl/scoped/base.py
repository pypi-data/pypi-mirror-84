class ConcernResponse:
    def __init__(self, result=None, errors=None):
        self.result = result
        if errors is None:
            self.errors = {}
        else:
            self.errors = errors

    def __repr__(self):
        return "result: %s, errors: %d" % (str(self.result), len(self.errors))

    def is_success(self):
        return len(self.errors) == 0

class BaseConcern:
    def __init__(self, attrs={}, **kwargs):
        if type(attrs) is dict:
            for attr in attrs:
                setattr(self, attr, attrs[attr])

        for attr in kwargs:
            setattr(self, attr, kwargs[attr])

        self.response = ConcernResponse()

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            return None

        return _missing()

    def execute(self):
        raise Exception("You have to override this method")

    def success(self, result = {}):
        self.response.result = result

        return self.response

    def error(self, errors = {}):
        if type(errors) is not dict:
            errors = { "errors": errors }

        errors["name"] = self.__class__

        self.response.errors = errors

        return self.response

    @classmethod
    def run(cls, *args, **kwargs):
        return cls(*args, **kwargs).execute()

class AsyncConcern(BaseConcern):
    async def execute(self):
        raise Exception("You have to override this method")

    @classmethod
    async def run(cls, *args, **kwargs):
        return await cls(*args, **kwargs).execute()
