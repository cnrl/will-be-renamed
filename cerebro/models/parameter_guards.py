from collections.abc import Iterable


class InstanceGuard:
    def __init__(self, cls):
        self.cls = cls

    def is_valid(self, instance):
        return isinstance(instance, self.cls)


class IterableGuard:
    def __init__(self, cls):
        self.element_guard = InstanceGuard(cls)

    def is_valid(self, instance):
        if not InstanceGuard(Iterable).is_valid(instance):
            return False

        return all([self.element_guard.is_valid(element) for element in instance])
