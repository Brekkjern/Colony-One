from typing import List


class Subject(object):
    """ The observed part in an observer system.

    The subject component should be attached to the object that generates the events.
    The subject component maintains a list of unique observers to call whenever an event is generated.
    Event handler methods of observers should be as minimal as possible to prevent delays in processing the main thread.
    """

    def __init__(self, observers: List[object] = None):
        if not observers:
            observers = []

        self.observers = observers

    def add_observer(self, observer: object):
        if not observer in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: object):
        self.observers.remove(observer)

    def notify_observers(self, entity, event):
        for observer in self.observers:
            observer.onNotify(entity, event)
