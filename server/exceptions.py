class ValueInputException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class ResourceNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RestaurantNotFoundException(ResourceNotFoundException):
    def __init__(self, message):
        super().__init__(message)
