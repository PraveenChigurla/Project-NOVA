from typing import Type, TypeVar, Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")

class DependencyResolutionError(Exception):
    """Raised when a dependency cannot be resolved."""
    pass

class ServiceLocator:
    """
    A lightweight, centralized Dependency Injection container.
    """
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable[[], Any]] = {}

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a singleton instance for an interface."""
        logger.debug(f"Registering instance for {interface.__name__}")
        self._services[interface] = instance

    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a factory function for an interface."""
        logger.debug(f"Registering factory for {interface.__name__}")
        self._factories[interface] = factory

    def resolve(self, interface: Type[T]) -> T:
        """Resolve an instance for the given interface."""
        if interface in self._services:
            return self._services[interface]
            
        if interface in self._factories:
            # Lazy initialize singleton from factory
            logger.debug(f"Lazy initializing {interface.__name__} from factory")
            instance = self._factories[interface]()
            self._services[interface] = instance
            return instance
            
        raise DependencyResolutionError(f"No implementation registered for {interface.__name__}")

    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._factories.clear()
