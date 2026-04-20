"""
Registry singleton que descubre y registra automáticamente todos los métodos
numéricos en el paquete `app.methods` usando pkgutil + importlib.

Para agregar un nuevo método: solo crear un archivo .py en app/methods/
con una clase que herede de NumericalMethod. El registry la detecta al arrancar.
"""
import importlib
import inspect
import pkgutil

from app.core.base_method import NumericalMethod


class MethodRegistry:
    """Singleton que mantiene un diccionario {name: clase} de métodos disponibles."""

    def __init__(self):
        self._methods: dict[str, type[NumericalMethod]] = {}

    def discover(self, package_name: str) -> None:
        """
        Importa todos los módulos del paquete indicado y registra
        automáticamente las subclases de NumericalMethod encontradas.
        """
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
                        # Clase abstracta incompleta, la ignoramos
                        pass

    def get(self, name: str) -> NumericalMethod:
        """Devuelve una instancia del método por su name. Lanza KeyError si no existe."""
        if name not in self._methods:
            raise KeyError(f"Método '{name}' no encontrado. Disponibles: {list(self._methods.keys())}")
        return self._methods[name]()

    def list_all(self) -> list[dict]:
        """Lista todos los métodos registrados con metadata completa."""
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
