from abc import ABC, abstractmethod

from src.models.universe_member import UniverseMember


class UniverseProvider(ABC):

    @abstractmethod
    def get_members(self) -> list[UniverseMember]:
        pass