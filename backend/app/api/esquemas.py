from typing import Optional, Union

from pydantic import BaseModel, ConfigDict

# Cuerpos de las peticiones. Los campos son opcionales y de tipo flexible a
# proposito: las rutas comprueban lo obligatorio y responden con los mismos
# mensajes que la version Flask. Aqui solo se documenta lo que se espera
# (aparece en /docs).

Entero = Optional[Union[int, str]]


class _Cuerpo(BaseModel):
    model_config = ConfigDict(extra="allow")


class DatosLogin(_Cuerpo):
    email: Optional[str] = None
    password: Optional[str] = None


class DatosRegistro(_Cuerpo):
    name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class DatosFavorito(_Cuerpo):
    id_game: Entero = None
    status: Optional[str] = None


class DatosNuevoComentario(_Cuerpo):
    id_game: Entero = None
    description: Optional[str] = None
    rating: Entero = None


class DatosEdicionComentario(_Cuerpo):
    description: Optional[str] = None
    rating: Entero = None


class DatosEdicionUsuario(_Cuerpo):
    id_user: Entero = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class DatosUsuarioObjetivo(_Cuerpo):
    id_user: Entero = None


class DatosCambioRol(_Cuerpo):
    id_user: Entero = None
    new_role: Optional[str] = None


class DatosCambioContrasena(_Cuerpo):
    current_password: Optional[str] = None
    new_password: Optional[str] = None
