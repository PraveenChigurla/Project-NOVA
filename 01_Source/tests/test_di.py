import pytest
from nova.core.di import ServiceLocator, DependencyResolutionError

class IDummyService:
    def do_work(self) -> str:
        pass

class DummyService(IDummyService):
    def do_work(self) -> str:
        return "done"

def test_service_locator_register_instance():
    locator = ServiceLocator()
    instance = DummyService()
    
    locator.register_instance(IDummyService, instance)
    resolved = locator.resolve(IDummyService)
    
    assert resolved is instance
    assert resolved.do_work() == "done"

def test_service_locator_register_factory():
    locator = ServiceLocator()
    
    # Factory should only be called once (singleton pattern)
    factory_calls = 0
    def factory():
        nonlocal factory_calls
        factory_calls += 1
        return DummyService()
        
    locator.register_factory(IDummyService, factory)
    
    assert factory_calls == 0
    resolved1 = locator.resolve(IDummyService)
    assert factory_calls == 1
    
    resolved2 = locator.resolve(IDummyService)
    assert factory_calls == 1
    assert resolved1 is resolved2

def test_service_locator_unregistered():
    locator = ServiceLocator()
    with pytest.raises(DependencyResolutionError):
        locator.resolve(IDummyService)
