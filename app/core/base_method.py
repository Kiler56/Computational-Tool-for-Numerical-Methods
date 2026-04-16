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

    @abstractmethod
    def solve(self, A: list, b: list) -> dict:
        """
        Resuelve el sistema Ax = b.

        Args:
            A: Matriz de coeficientes (list[list[float]]).
            b: Vector de términos independientes (list[float]).

        Returns:
            dict con al menos:
                - "solution": list[float]
                - "steps": list[dict]  (snapshots de cada paso)
                - "method": str        (self.name)
        """
        ...

    @staticmethod
    def _snapshot(matrix: list) -> list:
        """Copia profunda serializable de una matriz (o vector)."""
        return copy.deepcopy(matrix)
