from flask import request
from flask_limiter import Limiter


def clave_limite():
    try:
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass
    return f"ip:{request.remote_addr}"


limiter = Limiter(
    key_func=clave_limite,
    default_limits=[],
    storage_uri="memory://",
)
