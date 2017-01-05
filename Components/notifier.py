import logging
from typing import List

logger = logging.getLogger(__name__)



class Notifier(object):
    """ The observed part in an observer system.

    The subject component should be attached to the object that generates the events.
    The subject component maintains a list of unique observers to call whenever an event is generated.
    Event handler methods of observers should be as minimal as possible to prevent delays in processing the main thread.
    """

    def __init__(self, observers: List[object] = None):
        if observers:
            self.observers = observers
        else:
            self.observers = []

    def add_observer(self, observer: object):
        if not observer in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: object):
        self.observers.remove(observer)

    def notify_observers(self, entity, event):
        """Calls the observer_notify method of the observers

        If that method isn't defined an error is logged.
        """
        for observer in self.observers:
            try:
                observer.observer_notify(entity, event)
            except NameError:
                logger.error("Notifier: Undefined method on {0}. Event: {1}".format(entity, event))
