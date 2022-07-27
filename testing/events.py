class EventHandler:
    def __init__(self):
        self.events = {}

    def register(self, event_type, callback):
        if event_type not in self.events:
            self.events[event_type] = []

        self.events[event_type].append(callback)

    def unregister(self, event_type, callback):
        if event_type in self.events:
            self.events[event_type].remove(callback)

    def handle_event(self, event_type, *args, **kwargs):
        if event_type in self.events:
            for callback in self.events[event_type]:
                callback(*args, **kwargs)
        else:
            print("No event handler for", event_type)
