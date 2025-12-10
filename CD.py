class CD:    
    def __init__(self, id: int, name: str, size: float, encryption_speed: int,
                 occupied_space: float, session_count: int, session_type: str, **kwargs):
        self._id = id
        self._name = name
        self._size = size
        self._encryption_speed = encryption_speed
        self._occupied_space = occupied_space
        self._session_count = session_count
        self._session_type = session_type
        self._is_open = (session_type.lower() != 'finalized')

    # --- Properties ---
    @property
    def id(self) -> int: return self._id
    @property
    def name(self) -> str: return self._name
    @property
    def size(self) -> float: return self._size
    @property
    def encryption_speed(self) -> int: return self._encryption_speed
    @property
    def occupied_space(self) -> float: return self._occupied_space
    @property
    def session_count(self) -> int: return self._session_count
    @property
    def session_type(self) -> str: return self._session_type

    # --- Calculated Properties ---
    @property
    def getFreeSpace(self) -> float:
        return self._size - self._occupied_space

    @property
    def getOpenSession(self) -> bool:
        return self._is_open

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "size": self._size,
            "encryption_speed": self._encryption_speed,
            "occupied_space": self._occupied_space,
            "session_count": self._session_count,
            "session_type": self._session_type,
            # We include these for the UI, but __init__ will now safely ignore them if present
            "free_space": self.getFreeSpace,
            "is_open": self._is_open
        }