from typing import List, Optional
from xmlrpc.client import boolean

from CD import CD
from ICDRepository import ICDRepository

class CDService:
    def __init__(self, repository: ICDRepository):
        self._repository = repository

    def add(self, name: str, size: float, encryption_speed: int,
            occupied_space: float, session_count: int, session_type: str) -> bool:
        new_id = self._repository.get_next_id()
        new_cd = CD(new_id, name, size, encryption_speed, occupied_space, session_count, session_type)
        return self._repository.add(new_cd)

    def update_status(self, cd_id: int, is_finalized: bool) -> bool:
        """Updates the finalization status of a CD."""
        cd = self.find_by_id(cd_id)
        if cd:
            cd.set_finalized(is_finalized)
            return True
        return False

    def sortByName(self) -> List[CD]:
        return sorted(self._repository.getAll(), key=lambda cd: cd.name)

    def sortBySpeed(self) -> List[CD]:
        return sorted(self._repository.getAll(), key=lambda cd: cd.encryption_speed, reverse=True)

    def sortBySize(self) -> List[CD]:
        return sorted(self._repository.getAll(), key=lambda cd: cd.size, reverse=True)

    def filterByFreeSpace(self, min_space: float) -> List[CD]:
        return self._repository.getFreeSpace(min_space)
    
    def get_all_cds(self) -> List[CD]:
        return self._repository.getAll()

    def get_open_sessions(self) -> List[CD]:
        return self._repository.getOpenSessions()

    def find_by_id(self, cd_id: int) -> Optional[CD]:
        for cd in self._repository.getAll():
            if cd.id == cd_id:
                return cd
        return None
    
    def delete_cd(self, cd_id: int) -> bool:
        return self._repository.delete(cd_id)

    def save(self, filepath: str) -> bool:
        return self._repository.uploadData(filepath)

    def load(self, filepath: str) -> bool:
        return self._repository.loadData(filepath)