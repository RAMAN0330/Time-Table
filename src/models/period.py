from dataclasses import dataclass
from datetime import time
from typing import Optional

@dataclass
class Period:
    start_time: time
    end_time: time
    subject: str
    teacher: Optional[str] = None
    is_assembly: bool = False
    is_break: bool = False
    
    @property
    def duration_minutes(self) -> int:
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return end_minutes - start_minutes
    
    def __str__(self) -> str:
        if self.is_assembly:
            return "Assembly"
        elif self.is_break:
            return "Break"
        return f"{self.subject} ({self.teacher})"
