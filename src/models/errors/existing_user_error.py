class UserError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))


class InvalidPageError(UserError):
    pass

class InvalidLimitError(UserError):
    pass

class ExistingEmailError(UserError):
    pass

class UncompleteFieldsError(UserError):
    pass

class UserNotFoundError(UserError):
    pass

class NoModifyError(UserError):
    pass

class EmptyRequestError(UserError):
    pass

class UserNotExistError(UserError):
    pass