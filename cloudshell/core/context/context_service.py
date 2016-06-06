from abc import abstractmethod


class ContextBasedService(object):
    @abstractmethod
    def get_objects(self):
        pass

    @abstractmethod
    def context_started(self):
        pass

    @abstractmethod
    def context_ended(self, exc_type, exc_val, exc_tb):
        pass

    def __enter__(self):
        self.context_started()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context_ended(exc_type, exc_val, exc_tb)
