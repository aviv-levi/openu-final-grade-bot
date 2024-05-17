from abc import ABC, abstractmethod


class BotHandler(ABC):

    @abstractmethod
    def handle(self):
        pass
