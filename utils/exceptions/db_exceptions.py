class NoSessionException(Exception):
    def __init__(self, message='Database session is closed'):
        super().__init__(message)
