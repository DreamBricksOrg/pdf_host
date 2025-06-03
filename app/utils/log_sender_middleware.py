from fastapi import Request

def get_log_sender(request: Request):
    return request.app.state.log_sender
