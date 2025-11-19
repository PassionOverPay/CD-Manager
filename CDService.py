from typing import List, Optional
from xmlrpc.client import boolean

from CD import CD
from ICDRepository import ICDRepository

class CDService:
    def __init__(self, repository: ICDRepository):
        self._repository = repository

    def add(self, name: str, size: float, encryption_speed: int,
            occupied_space: float, session_count: int, session_type: str) -> bool:
        print("Service: Adding new CD...")
        new_id = self._repository.get_next_id()
        new_cd = CD(new_id, name, size, encryption_speed, occupied_space, session_count, session_type)
        return self._repository.add(new_cd)

    def sortByName(self) -> List[CD]:
        print("Service: Sorting by name...")
        all_cds = self._repository.getAll()
        return sorted(all_cds, key=lambda cd: cd.name)

    def sortBySpeed(self) -> List[CD]:
        print("Service: Sorting by speed...")
        all_cds = self._repository.getAll()
        return sorted(all_cds, key=lambda cd: cd.encryption_speed, reverse=True)

    def sortBySize(self) -> List[CD]:
        print("Service: Sorting by size...")
        all_cds = self._repository.getAll()
        return sorted(all_cds, key=lambda cd: cd.size, reverse=True)

    def filterByFreeSpace(self, min_space: float) -> List[CD]:
        print(f"Service: Filtering by free space > {min_space}...")
        return self._repository.getFreeSpace(min_space)
    
    def get_all_cds(self) -> List[CD]:
        return self._repository.getAll()

    def find_by_id(self, cd_id: int) -> Optional[CD]:
        for cd in self._repository.getAll():
            if cd.id == cd_id:
                return cd
        return None
