from dataclasses import dataclass
from typing import List, Dict, Union
from datetime import time

@dataclass
class Teacher:
    name: str
    subjects: List[str]
    classes: List[str]
    availability: Dict[str, List[List[Union[str, time]]]]  # Day -> List of [start_time, end_time]
    
    def __post_init__(self):
        """Convert time strings to time objects if they aren't already"""
        from src.utils.helpers import parse_time
        
        for day, slots in self.availability.items():
            converted_slots = []
            for slot in slots:
                converted_slots.append([
                    parse_time(slot[0]) if isinstance(slot[0], str) else slot[0],
                    parse_time(slot[1]) if isinstance(slot[1], str) else slot[1]
                ])
            self.availability[day] = converted_slots
    
    def is_available(self, day: str, period_start: time, period_end: time) -> bool:
        """Check if teacher is available for a given time slot."""
        if day not in self.availability:
            return False
            
        for start, end in self.availability[day]:
            # Convert minutes since midnight for proper comparison
            slot_start_mins = start.hour * 60 + start.minute
            slot_end_mins = end.hour * 60 + end.minute
            period_start_mins = period_start.hour * 60 + period_start.minute
            period_end_mins = period_end.hour * 60 + period_end.minute
            
            if slot_start_mins <= period_start_mins and period_end_mins <= slot_end_mins:
                return True
        return False
    
    def can_teach_subject(self, subject: str) -> bool:
        """Check if teacher can teach a subject."""
        return subject in self.subjects
    
    def __str__(self) -> str:
        return f"{self.name} ({', '.join(self.subjects)})"
