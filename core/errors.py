class BaseError(Exception):
    status_code = 500
    message = "Unhandled error"
    errors = []
    field = ""

    def __init__(self, message="", field: str = "", errors: list = []):
        if message:
            self.message = message
        if field:
            self.field = field
        if errors:
            self.errors = errors

    def __str__(self):
        return str(self.message)
