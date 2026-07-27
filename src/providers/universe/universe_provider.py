from abc import ABC, abstractmethod

from models.universe_member import UniverseMember


class UniverseProvider(ABC):

    @abstractmethod
    def get_members(self) -> list[UniverseMember]:
        pass