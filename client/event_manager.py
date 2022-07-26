"""Implements the event manager"""


from typing import Any, Callable, Generic, Hashable, TypeVar
from collections import defaultdict

CallableT = TypeVar("CallableT", bound=Callable)
KeyT = TypeVar("KeyT", bound=Hashable)


class EventManager(Generic[KeyT]):
    """Manages the events using handler functions"""

    handlers: dict[KeyT, list[tuple[Callable, bool]]]

    def __init__(self) -> None:
        self.handlers = defaultdict(list)

    def add_handler(self, name: KeyT, func: Callable, with_name: bool = False):
        """Adds handler to the event manager"""
        self.handlers[name].append((func, with_name))

    def on(self, name: KeyT, with_name: bool = False) -> Callable[[CallableT], CallableT]:
        """Defines a wrapper for event handlers"""
        def decorator(func: CallableT) -> CallableT:
            self.add_handler(name, func, with_name)
            return func

        return decorator

    def emit(self, name: KeyT, *args, **kwargs) -> tuple[Any, ...]:
        """
        Emits the event for handlers to work on

        Parameters
        ----------
        name : Hashable
            name of the event
        *args
            arbitrary list of arguments emitted with the event
        **kwargs
            arbitrary list of keywords emitted with the event

        Returns
        -------
        tuple
            contains returns from the handlers associated with the event `name`
        """
        return tuple(
            func(name, *args, **kwargs) if with_name else func(*args, **kwargs)
            for func, with_name in self.handlers[name]
        )


event_manager = EventManager[int | str]()
