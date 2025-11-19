class CD:
    def __init__(self, id: int, name: str, size: float, encryption_speed: int,
                 occupied_space: float, session_count: int, session_type: str):
        self._id = id
        self._name = name
        self._size = size 
        self._encryption_speed = encryption_speed
        if occupied_space <= size:
            self._occupied_space = occupied_space
        else:
            print(f"Error: Occupied space ({occupied_space}) cannot exceed total size ({size}).")
            self._occupied_space = size
        self._session_count = session_count
        self._session_type = session_type
        self._is_open = (session_type.lower() != 'finalized')

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> float:
        return self._size

    @property
    def encryption_speed(self) -> int:
        return self._encryption_speed

    @property
    def occupied_space(self) -> float:
        return self._occupied_space

    @property
    def session_count(self) -> int:
        return self._session_count

    @property
    def session_type(self) -> str:
        return self._session_type

    @name.setter
    def name(self, value: str):
        if value:  
            self._name = value
        else:
            print("Error: Name cannot be empty.")

    @size.setter
    def size(self, value: float):
        self._size = value

    @encryption_speed.setter
    def encryption_speed(self, value: int):
        self._encryption_speed = value

    @occupied_space.setter
    def occupied_space(self, value: float):
        if value <= self._size:
            self._occupied_space = value
        else:
            print(f"Error: Occupied space ({value}) cannot exceed total size ({self._size}).")

    @session_count.setter
    def session_count(self, value: int):
        self._session_count = value

    @session_type.setter
    def session_type(self, value: str):
        self._session_type = value
        self._is_open = (value.lower() != 'finalized')


    @property
    def getFreeSpace(self) -> float:
        return self._size - self._occupied_space

    @property
    def getOpenSession(self) -> bool:
        return self._is_open

    def to_dict(self):
        """Returns a dictionary representation of the CD for JSON serialization."""
        return {
            "id": self._id,
            "name": self._name,
            "size": self._size,
            "encryption_speed": self._encryption_speed,
            "occupied_space": self._occupied_space,
            "session_count": self._session_count,
            "session_type": self._session_type
        }

    def __str__(self):
        return f"CD[ID={self.id}, Name='{self.name}', Size={self.size}MB, Free={self.getFreeSpace}MB]"

