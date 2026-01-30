class CD:
    """
    Represents the core data object (Model) for a single CD.
    """
    def __init__(self, id: int, name: str, size: float, encryption_speed: int,
                 occupied_space: float, session_count: int, session_type: str, **kwargs):
        self._id = id
        self._name = name
        self._size = size
        self._encryption_speed = encryption_speed
        self._occupied_space = occupied_space
        self._session_count = session_count
        
        # Sanitize session_type
        self._session_type = str(session_type).strip()
        
        # A CD is considered open if it is NOT finalized
        self._is_open = (self._session_type.lower() != 'finalized')

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

    # --- Methods ---
    def set_finalized(self, is_finalized: bool):
        """Updates the session type based on the boolean flag."""
        if is_finalized:
            self._session_type = "Finalized"
            self._is_open = False
        else:
            # If un-finalizing, default to "Data" if it was "Finalized"
            if self._session_type.lower() == "finalized":
                self._session_type = "Data"
            self._is_open = True

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "size": self._size,
            "encryption_speed": self._encryption_speed,
            "occupied_space": self._occupied_space,
            "session_count": self._session_count,
            "session_type": self._session_type,
            "free_space": self.getFreeSpace,
            "is_open": self._is_open
        }
