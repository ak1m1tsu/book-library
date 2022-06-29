class Error(Exception):
    '''Base class for other exceptions'''
    pass


class NotFoundError(Error):
    '''Raised when the object not found'''
    pass


class AlreadyExistsError(Error):
    '''Raised when the object already exists in database'''
    pass


class ClientExists(Error):
    '''Raised when rpc client alrady exists in server client list'''
    pass
