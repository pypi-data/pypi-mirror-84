"""Contains the ContainerDefinition and Container classes."""
import inspect
from dataclasses import Field, dataclass
from typing import (Any, Awaitable, Callable, Mapping, MutableMapping,
                    Optional, Sequence, Tuple, Type, Union, cast)

service = dataclass

Key = Union[Type, str]
Factory = Callable[["Container"], Any]
SyncCleanup = Callable[[Any], None]
AsyncCleanup = Callable[[Any], Awaitable[None]]
Cleanup = Union[SyncCleanup, AsyncCleanup]


class Container:
    """DependencyInjection container instance."""

    def __init__(self, container_definition: "ContainerDefinition") -> None:
        self.container_definition = container_definition
        self.services: MutableMapping[str, Any] = {}

    def has(self, key: Key) -> bool:
        key = _get_key(key)
        return key in self.services

    def get(self, key: Key) -> Any:
        key = _get_key(key)
        if key not in self.services:
            self.services[key] = self.container_definition.get(key)(self)
        return self.services[key]

    async def reset(self, key: Key) -> "Container":
        key = _get_key(key)
        await self.cleanup(key)
        del self.services[key]
        return self

    async def reset_all(self) -> "Container":
        await self.cleanup_all()
        self.services = {}
        return self

    async def cleanup(self, key: Key):
        """Cleanup a single service if it has been booted and it has a cleanup function
        registered.
        """
        key = _get_key(key)
        if key not in self.services:
            return

        cleanup = self.container_definition.get_cleanup(key)

        if not cleanup:
            return

        service = self.services[key]
        result = cleanup(service)
        if inspect.isawaitable(result):
            await cast(Awaitable[Any], result)

    async def cleanup_all(self):
        """Iterate through all services that have been created, and call the associated cleanup
        method for that service, if there is one.
        """
        for key in self.services:
            await self.cleanup(key)
        return


class ContainerDefinition:
    """Maps dependency keys to factories."""

    def __init__(self, *, allow_overwrite: bool = False) -> None:
        self.allow_overwrite: bool = allow_overwrite
        self.services: MutableMapping[str, Factory] = {}
        self.cleanup: MutableMapping[str, Cleanup] = {}

    def add_factory(
        self, key: Key, factory: Factory, *, cleanup: Optional[Cleanup] = None
    ) -> "ContainerDefinition":
        """Register a service in the container with an explicit key and factory."""
        key = _get_key(key)

        if not self.allow_overwrite:
            if key in self.services:
                raise KeyError(f"Key {key} already added to container")

        self.services[key] = factory

        if cleanup:
            self.cleanup[key] = cleanup

        return self

    def add_key_list(
        self,
        key: Key,
        dependencies: Sequence[Key],
        factory: Optional[Factory] = None,
        *,
        cleanup: Optional[Cleanup] = None,
    ) -> "ContainerDefinition":
        """Register a service in the container with an explicit key and a list of keys of
        dependencies.
        """
        if isinstance(key, str):
            if not factory:
                raise TypeError("factory cannot be None when key is a string")
        else:
            if not factory:
                factory = key

        return self.add_factory(
            key,
            _key_list_factory([_get_key(k) for k in dependencies], factory),
            cleanup=cleanup,
        )

    def add_service(
        self, cls: Type, *, cleanup: Optional[Cleanup] = None,
    ) -> "ContainerDefinition":
        """Register a type wrapped in @service. All of the typed properties on the class will
        be used as the dependency list.
        """
        dependency_dict: Mapping[str, Field] = cls.__dataclass_fields__
        dependency_keys = [_get_key(field.type) for field in dependency_dict.values()]
        return self.add_key_list(cls, dependency_keys, cleanup=cleanup)

    def add(
        self,
        key: Key,
        factory: Optional[
            Union[Factory, Sequence[Key], Tuple[Sequence[Key], Factory]]
        ] = None,
        *,
        cleanup: Optional[Cleanup] = None,
    ) -> "ContainerDefinition":
        """Catch all method that will call either add_factory, add_key_list, or add_service
        depending on the arguments.

        add_service if key is a Type and factory is None
        add_factory if factory is a Factory
        add_key_list if factory is a (Factory, Sequence[Key]) tuple
        """
        if factory is None:
            if isinstance(key, str):
                raise TypeError(
                    "key must be a Type if dependencies and factory are not given"
                )
            return self.add_service(key, cleanup=cleanup)
        if callable(factory):
            return self.add_factory(key, factory, cleanup=cleanup)
        if isinstance(factory, tuple):
            (dependencies, factory_fn) = factory
            return self.add_key_list(key, dependencies, factory_fn, cleanup=cleanup)
        return self.add_key_list(key, factory, cleanup=cleanup)

    def get(self, key: str) -> Factory:
        return self.services[key]

    def get_container(self) -> Container:
        return Container(self)

    def get_cleanup(self, key: str) -> Optional[Cleanup]:
        return self.cleanup.get(key, None)


def _key_list_factory(dependencies: Sequence[str], factory: Callable) -> Factory:
    def build(container: Container) -> Any:
        return factory(*[container.get(key) for key in dependencies])

    return build


def _get_key(key: Key) -> str:
    if isinstance(key, str):
        return key
    return key.__module__ + "." + key.__name__
