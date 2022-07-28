from typing import Any, Callable, Generic, Hashable, TypeVar
from collections import defaultdict
import asyncio

CallableT = TypeVar("CallableT", bound=Callable)
KeyT = TypeVar("KeyT", bound=Hashable)


class AsyncEventManager(Generic[KeyT]):
    """Manages the events using async handler functions"""

    handlers: dict[KeyT, list[tuple[Callable, bool]]]
    _loop: asyncio.AbstractEventLoop | None

    def __init__(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self._loop = loop
        self.handlers = defaultdict(list)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None:
            self._loop = asyncio.get_event_loop_policy().get_event_loop()
        return self._loop

    async def emit(self, name: KeyT, *args, **kwargs) -> tuple[Any, ...]:
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
        return await asyncio.gather(
            *(
                func(name, *args, **kwargs) if with_name else func(*args, **kwargs)
                for func, with_name in self.handlers[name]
            )
        )

    def dispatch(self, name: KeyT, *args, **kwargs):
        self.loop.create_task(self.emit(name, *args, **kwargs))

    def on(self, name: KeyT, with_name: bool = False) -> Callable[[CallableT], CallableT]:
        """Defines a wrapper for event handlers"""  # not actually wrapper
        def decorator(func: CallableT) -> CallableT:
            self.handlers[name].append((func, with_name))
            return func
        return decorator

    def add_handler(self, name: KeyT, func: Callable, with_name: bool = False):
        """Adds handler to the event manager"""
        self.handlers[name].append((func, with_name))


event_manager = AsyncEventManager[str]()
