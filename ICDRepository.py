from abc import ABC, abstractmethod
from typing import List

from CD import CD

class ICDRepository(ABC):
    @abstractmethod
    def add(self, cd: CD) -> bool:
        pass

    @abstractmethod
    def delete(self, cd_id: int) -> bool:
        pass

    @abstractmethod
    def getAll(self) -> List[CD]:
        pass

    @abstractmethod
    def getFreeSpace(self, min_space: float) -> List[CD]:
        pass
    
    @abstractmethod
    def getOpenSessions(self) -> List[CD]:
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Expose ID generation through the interface to avoid direct attribute access."""
        pass

    @abstractmethod
    def loadData(self, filepath: str) -> bool:
        pass

    @abstractmethod
    def uploadData(self, filepath: str) -> bool:
        pass
