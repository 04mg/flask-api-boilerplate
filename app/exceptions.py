def handle_http_exception(e):
    return {
        "message": e.description,
    }, e.code
