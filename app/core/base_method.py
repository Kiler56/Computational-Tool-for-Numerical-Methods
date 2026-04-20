"""
Clase abstracta base para todos los métodos numéricos.
Cada método concreto hereda de NumericalMethod e implementa solve().
"""
import copy
from abc import ABC, abstractmethod


class NumericalMethod(ABC):
    """Interfaz base que todo método numérico debe implementar."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identificador único del método (slug), e.g. 'gaussian_simple'."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción legible del método, e.g. 'Eliminación Gaussiana Simple'."""
        ...

    @property
    @abstractmethod
    def instructions(self) -> dict:
        """Instrucciones de uso en formato HTML. Retorna dict con claves 'es' y 'en'."""
        ...

    @property
    def method_type(self) -> str:
        """Tipo de método: 'linear_system' o 'root'.
        Subclases pueden sobreescribir. Por defecto 'linear_system'.
        """
        return "linear_system"

    @property
    def params_schema(self) -> list:
        """Define los parámetros que el formulario del solver debe mostrar.
        Retorna lista de dicts: [{"key": "a", "label_es": "...", "label_en": "...", "type": "float", "default": 0}, ...]
        Solo relevante para métodos de tipo 'root'.
        """
        return []

    @abstractmethod
    def solve(self, *args, **kwargs) -> dict:
        """
        Resuelve el problema numérico.

        Para linear_system: solve(A, b) -> Ax = b.
        Para root: solve(expr, params) -> f(x) = 0.

        Returns:
            dict con al menos:
                - "solution": resultado
                - "steps": list[dict]
                - "method": str (self.name)
        """
        ...

    @staticmethod
    def _snapshot(data: list) -> list:
        """Copia profunda serializable."""
        return copy.deepcopy(data)
