from typing import List, Optional
import os
import json

from CD import CD
from ICDRepository import ICDRepository

class CDRepository(ICDRepository):

    def __init__(self):
        self._cdList: List[CD] = []
        self._nextId: int = 1 

    def get_next_id(self) -> int:
        return self._nextId

    def add(self, cd: CD) -> bool:
        print(f"Repository: Adding CD with ID {cd.id}...")
        self._cdList.append(cd)
        self._nextId += 1
        return True

    def delete(self, cd_id: int) -> bool:
        print(f"Repository: Deleting CD with ID {cd_id}...")
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
        """Corresponds to +getAll(): List<CD>"""
        return self._cdList

    def getFreeSpace(self, min_space: float) -> List[CD]:
        print(f"Repository: Getting CDs with free space > {min_space}...")
        result = [cd for cd in self._cdList if cd.getFreeSpace > min_space]
        return result

    def getOpenSessions(self) -> List[CD]:
        print("Repository: Getting CDs with open sessions...")
        result = [cd for cd in self._cdList if cd.getOpenSession]
        return result

    def loadData(self, filepath: str) -> bool:
        print(f"Repository: Attempting to load data from {filepath}...")
        
        if not os.path.exists(filepath):
            print("Info: No save file found. Starting with an empty library.")
            return True 

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self._cdList = []
            loaded_cds = data.get("cds", [])
            for cd_data in loaded_cds:
                self._cdList.append(CD(**cd_data))
            
            self._nextId = data.get("nextId", len(self._cdList) + 1)
            print(f"Successfully loaded {len(self._cdList)} CDs.")
            return True
        except (IOError, json.JSONDecodeError, TypeError) as e:
            print(f"Error: Failed to load data from {filepath}. Error: {e}")
            return False

    def uploadData(self, filepath: str) -> bool:
        # save to a JSON file
        print(f"Repository: Saving data to {filepath}...")
        try:
            data_to_save = [cd.to_dict() for cd in self._cdList]
            
            payload = {
                "cds": data_to_save,
                "nextId": self._nextId
            }

            with open(filepath, 'w') as f:
                json.dump(payload, f, indent=4)
            
            print(f"Successfully saved {len(self._cdList)} CDs.")
            return True
        except IOError as e:
            print(f"Error: Failed to save data to {filepath}. Error: {e}")
            return False
