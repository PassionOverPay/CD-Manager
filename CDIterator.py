from typing import List, Optional

from CD import CD

class CDIterator:
    def __init__(self, cd_list: List[CD]):
        self._cd_list = cd_list
        self._index = 0

    def hasNext(self) -> bool:
        return self._index < len(self._cd_list)

    def next(self) -> Optional[CD]:
        if self.hasNext():
            cd = self._cd_list[self._index]
            self._index += 1
            return cd
        return None