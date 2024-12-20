from dataclasses import dataclass
from datetime import time
from typing import List, Tuple

@dataclass
class ClassInfo:
    name: str
    division: str
    start_time: time
    end_time: time
    breaks: List[Tuple[time, time]]
    
    @property
    def class_name(self) -> str:
        """Return formatted class name with division."""
        return f"{self.name}-{self.division}"
