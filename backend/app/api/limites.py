from fastapi import Request
from slowapi import Limiter

from app.api.seguridad import leer_identidad


def clave_limite(request: Request):
    # Por usuario si lleva token valido; si no, por IP (como en Flask)
    identidad = leer_identidad(request, obligatorio=False)
    if identidad:
        return f"user:{identidad}"
    ip = request.client.host if request.client else "desconocida"
    return f"ip:{ip}"


# En memoria: con varios workers cada uno lleva su propia cuenta
limiter = Limiter(key_func=clave_limite, storage_uri="memory://", key_style="endpoint")
