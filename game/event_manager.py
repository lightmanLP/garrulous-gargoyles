from typing import Any, Callable, Generic, Hashable, TypeVar
from collections import defaultdict

CallableT = TypeVar("CallableT", bound=Callable)
KeyT = TypeVar("KeyT", bound=Hashable)


class EventManager(Generic[KeyT]):
    handlers: dict[KeyT, list[tuple[Callable, bool]]]

    def __init__(self) -> None:
        self.handlers = defaultdict(list)

    def add_handler(self, name: KeyT, func: Callable, with_name: bool = False):
        self.handlers[name].append((func, with_name))

    def on(self, name: KeyT, with_name: bool = False) -> Callable[[CallableT], CallableT]:
        def decorator(func: CallableT) -> CallableT:
            self.add_handler(name, func, with_name)
            return func
        return decorator

    def emit(self, name: KeyT, *args, **kwargs) -> tuple[Any, ...]:
        return tuple(
            func(name, *args, **kwargs) if with_name else func(*args, **kwargs)
            for func, with_name in self.handlers[name]
        )


event_manager = EventManager[int | str]()
