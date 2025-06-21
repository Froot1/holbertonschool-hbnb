from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base class for a repository.
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Get an object from the repository by its ID.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Get all objects from the repository.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object by a specific attribute.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object in the repository.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object from the repository by its ID.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository.
    """

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the in-memory storage.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Get an object from the in-memory storage by its ID.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Get all objects from the in-memory storage.
        """
        return list(self._storage.values())

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object from the in-memory storage by a specific attribute.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def update(self, obj_id, **data):
        """
        Update an object in the in-memory storage.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Delete an object from the in-memory storage by its ID.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
