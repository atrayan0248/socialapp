def api_response(status: bool = False, error: str = None, data: dict = None, message: str = 'Failure'):
    return {
        'status': status,
        'message': message if not status else 'Success',
        'data': data if not error else None,
        'error': error if not data else None,
    }
