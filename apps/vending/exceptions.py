class OrderException(Exception):
    def __init__(self, error: str = "Balance or quantity validation failed") -> None:
        self.error = error
