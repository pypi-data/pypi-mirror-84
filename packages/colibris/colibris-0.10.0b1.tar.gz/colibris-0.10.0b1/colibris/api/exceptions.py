class APIException(Exception):
    pass


class BaseJSONException(APIException):
    def __init__(self, code, message, status, details=None):
        self.code = code
        self.message = message
        self.details = details
        self.status = status

    def __str__(self):
        return self.code


class InvalidRequest(BaseJSONException):
    def __init__(self, code, message):
        super().__init__(code, message, status=400)


class SchemaError(BaseJSONException):
    def __init__(self, details):
        super().__init__(
            status=400,
            code='schema_error',
            message='Some of the supplied fields are invalid.',
            details=details
        )


class JSONParseError(InvalidRequest):
    def __init__(self):
        super().__init__(code='parse_error', message='JSON parse error')


class UnauthenticatedException(BaseJSONException):
    def __init__(self):
        super().__init__(code='unauthenticated', message='The request cannot be associated to an account.', status=401)


class ForbiddenException(BaseJSONException):
    def __init__(self):
        super().__init__(code='forbidden', message='Access to requested resource is forbidden.', status=403)


class NotFoundException(BaseJSONException):
    def __init__(self, resource='resource'):
        super().__init__('not_found',
                         'The requested {} cannot be found.'.format(resource),
                         status=404)


class DuplicateModelException(InvalidRequest):
    def __init__(self, model, field):
        super().__init__('duplicate_{}'.format(field),
                         'A {} with this {} already exists.'.format(model._meta.name, field))


class ModelNotFoundException(NotFoundException):
    def __init__(self, model):
        super().__init__(model._meta.name)
