from abc import ABC, abstractmethod
from django.http import HttpRequest


class ImageStorage(ABC):
    @abstractmethod
    def store(self, request: HttpRequest) -> str:
        """Almacena la imagen y devuelve la URL pública (o '' si falla)."""
        raise NotImplementedError
