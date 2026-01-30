from abc import ABC, abstractmethod
from typing import List, Optional
import json
import os
import streamlit as st

from CD import CD

class ICDRepository(ABC):
    @abstractmethod
    def add(self, cd: CD) -> bool: pass
    @abstractmethod
    def delete(self, cd_id: int) -> bool: pass
    @abstractmethod
    def getAll(self) -> List[CD]: pass
    @abstractmethod
    def getFreeSpace(self, min_space: float) -> List[CD]: pass
    @abstractmethod
    def getOpenSessions(self) -> List[CD]: pass
    @abstractmethod
    def get_next_id(self) -> int: pass
    @abstractmethod
    def loadData(self, filepath: str) -> bool: pass
    @abstractmethod
    def uploadData(self, filepath: str) -> bool: pass

class CDRepository(ICDRepository):
    def __init__(self):
        self._cdList: List[CD] = []
        self._nextId: int = 1

    def get_next_id(self) -> int:
        return self._nextId

    def add(self, cd: CD) -> bool:
        self._cdList.append(cd)
        self._nextId += 1
        return True

    def delete(self, cd_id: int) -> bool:
        cd_to_delete = self.deleteCD(cd_id)
        if cd_to_delete:
            self._cdList.remove(cd_to_delete)
            return True
        return False

    def deleteCD(self, cd_id: int) -> Optional[CD]:
        for cd in self._cdList:
            if cd.id == cd_id:
                return cd
        return None

    def getAll(self) -> List[CD]:
        return self._cdList

    def getFreeSpace(self, min_space: float) -> List[CD]:
        return [cd for cd in self._cdList if cd.getFreeSpace > min_space]

    def getOpenSessions(self) -> List[CD]:
        return [cd for cd in self._cdList if cd.getOpenSession]

    def loadData(self, filepath: str) -> bool:
        if not os.path.exists(filepath):
            return True 
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self._cdList = []
            loaded_cds = data.get("cds", [])
            for cd_data in loaded_cds:
                self._cdList.append(CD(**cd_data))
            
            self._nextId = data.get("nextId", len(self._cdList) + 1)
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def uploadData(self, filepath: str) -> bool:
        try:
            data_to_save = [cd.to_dict() for cd in self._cdList]
            payload = {"cds": data_to_save, "nextId": self._nextId}
            with open(filepath, 'w') as f:
                json.dump(payload, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
