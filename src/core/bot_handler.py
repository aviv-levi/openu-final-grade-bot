from abc import ABC, abstractmethod


class BotHandler(ABC):

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def run(self):
        pass
