class DomainError(Exception):
    def __init__(self, code: str, message: str, status: int = 422, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details or []

    def payload(self):
        return {"error": {"code": self.code, "message": self.message, "details": self.details}}
