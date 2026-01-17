from kittyk.api.schemas import BaseError


class InternalServerError(BaseError):
    title: str = "Internal Server Error"
    message: str = "An unexpected error occurred on the server."
    status_code: int = 500

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()


class ValidationError(BaseError):
    title: str = "Validation Error"
    message: str = "One or more validation errors occurred."
    status_code: int = 422

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()


class ConflictError(BaseError):
    title: str = "Conflict"
    message: str = "The request could not be completed due to a conflict with the current state of the resource."
    status_code: int = 409

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()


class NotFoundError(BaseError):
    title: str = "Not Found"
    message: str = "The requested resource was not found."
    status_code: int = 404

    def __init__(self, resource: str = "resource"):
        self.message = f"The requested {resource} was not found."

        super().__init__()


class ForbiddenError(BaseError):
    title: str = "Forbidden"
    message: str = "You do not have permission to access this resource."
    status_code: int = 403

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()


class PaymentRequiredError(BaseError):
    title: str = "Payment Required"
    message: str = "Payment is required to access this resource."
    status_code: int = 402

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()


class UnauthorizedError(BaseError):
    title: str = "Unauthorized"
    message: str = "You must be authenticated to access this resource."
    status_code: int = 401

    def __init__(self, *, title: str = None, message: str = None):
        if title:
            self.title = title

        if message:
            self.message = message

        super().__init__()
