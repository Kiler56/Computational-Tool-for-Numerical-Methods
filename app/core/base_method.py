"""
Abstract base class for all numerical methods.
Concrete methods inherit from NumericalMethod and implement solve().
"""
import copy
from abc import ABC, abstractmethod


class NumericalMethod(ABC):
    """Base interface every numerical method must implement."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique method slug, e.g. 'gaussian_simple'."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable method name."""
        ...

    @property
    @abstractmethod
    def instructions(self) -> dict:
        """Usage instructions as HTML; dict with keys 'es' and 'en'."""
        ...

    @property
    def method_type(self) -> str:
        """One of: 'linear_system', 'root', 'interpolation'. Default 'linear_system'."""
        return "linear_system"

    @property
    def params_schema(self) -> list:
        """Root-method form fields: [{"key", "label_es", "label_en", "type", "default"}, ...]."""
        return []

    @property
    def requires_vector_b(self) -> bool:
        """If False, the UI hides vector b and the API may default it to zeros."""
        return True

    @abstractmethod
    def solve(self, *args, **kwargs) -> dict:
        """
        Solve the numerical problem.

        linear_system: solve(A, b) for Ax = b.
        root: solve(expr, params) for f(x) = 0.
        interpolation: solve(points, x_eval=...) with points as [[x, y], ...].

        Returns:
            dict with at least "solution", "steps", "method".
        """
        ...

    @staticmethod
    def _snapshot(data: list) -> list:
        """Deep copy for serialization."""
        return copy.deepcopy(data)
