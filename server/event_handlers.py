from .event_manager import event_manager


@event_manager.on("enter")
async def print_hello(*args, **kwargs):
    print("Hello World!")


@event_manager.on("leave")
async def print_bye(*args, **kwargs):
    print("Goodbye World!")
