class GeocoderException(Exception):
    pass


class GeocoderHttpException(GeocoderException):
    def __init__(self, message='Database session is closed'):
        super().__init__(message)


class GeocoderToponymNotFoundException(GeocoderException):
    def __init__(self, message='Database session is closed'):
        super().__init__(message)
