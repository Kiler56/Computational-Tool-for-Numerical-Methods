"""
Singleton registry that discovers numerical methods in `app.methods` via pkgutil.

To add a method: create one module under app/methods/ with a NumericalMethod subclass.
"""
import importlib
import inspect
import pkgutil

from app.core.base_method import NumericalMethod


class MethodRegistry:
    """Singleton holding {slug: class} for registered methods."""

    def __init__(self):
        self._methods: dict[str, type[NumericalMethod]] = {}

    def discover(self, package_name: str) -> None:
        """Import submodules and register NumericalMethod subclasses."""
        package = importlib.import_module(package_name)
        for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_name = f"{package_name}.{module_name}"
            module = importlib.import_module(full_name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, NumericalMethod)
                    and obj is not NumericalMethod
                    and hasattr(obj, "name")
                ):
                    try:
                        instance = obj()
                        self._methods[instance.name] = obj
                    except TypeError:
                        # Incomplete abstract class — skip
                        pass

    def get(self, name: str) -> NumericalMethod:
        """Return a method instance by slug; raises KeyError if missing."""
        if name not in self._methods:
            raise KeyError(f"Method '{name}' not found. Available: {list(self._methods.keys())}")
        return self._methods[name]()

    def list_all(self) -> list[dict]:
        """List registered methods with metadata."""
        result = []
        for name, cls in self._methods.items():
            instance = cls()
            result.append({
                "name": instance.name,
                "description": instance.description,
                "method_type": instance.method_type,
                "params_schema": instance.params_schema,
            })
        return result


# Singleton global
registry = MethodRegistry()
