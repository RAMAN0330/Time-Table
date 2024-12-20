from typing import Dict, List, Optional
from datetime import time, timedelta
import pandas as pd

from src.models.class_info import ClassInfo
from src.models.period import Period
from src.models.teacher import Teacher
from src.config import (
    PERIOD_DURATION,
    ASSEMBLY_DAY,
    ASSEMBLY_TIME,
    WORKING_DAYS,
    MIN_PERIODS_PER_DAY,
    MAX_PERIODS_PER_DAY,
    CLASS_TIMINGS,
    BREAK_TIMINGS,
    SUBJECTS
)

class TimetableGenerator:
    def __init__(
        self,
        class_info: ClassInfo,
        teachers: List[Teacher],
        subject_distribution: Dict[str, int]
    ):
        self.class_info = class_info
        self.teachers = teachers
        self.subject_distribution = subject_distribution
        self.timetable: Dict[str, List[Period]] = {day: [] for day in WORKING_DAYS}
        self.remaining_periods = dict(subject_distribution)
        
        # Validate subjects
        valid_subjects = SUBJECTS[class_info.name]
        for subject in subject_distribution.keys():
            if subject not in valid_subjects:
                raise ValueError(f"Invalid subject '{subject}' for class {class_info.name}")
    
    def generate_timetable(self) -> Dict[str, List[Period]]:
        """Generate a weekly timetable for the class."""
        for day in WORKING_DAYS:
            day_schedule = self._generate_day_schedule(day)
            if not day_schedule:
                raise ValueError(f"Could not generate valid schedule for {day}")
            self.timetable[day] = day_schedule
            
        # Verify all subjects are distributed
        if any(count > 0 for count in self.remaining_periods.values()):
            raise ValueError("Could not distribute all required periods")
            
        return self.timetable
    
    def _generate_day_schedule(self, day: str) -> List[Period]:
        """Generate schedule for a single day."""
        periods: List[Period] = []
        current_time = self.class_info.start_time
        
        while current_time < self.class_info.end_time:
            # Check for assembly
            if day == ASSEMBLY_DAY and self._time_equals(current_time, ASSEMBLY_TIME):
                period = Period(
                    start_time=current_time,
                    end_time=self._add_minutes(current_time, PERIOD_DURATION.seconds // 60),
                    subject="Assembly",
                    is_assembly=True
                )
                periods.append(period)
                current_time = period.end_time
                continue
            
            # Check for breaks
            is_break = False
            for break_start, break_end in BREAK_TIMINGS[self.class_info.name]:
                if self._time_equals(current_time, break_start):
                    period = Period(
                        start_time=break_start,
                        end_time=break_end,
                        subject="Break",
                        is_break=True
                    )
                    periods.append(period)
                    current_time = break_end
                    is_break = True
                    break
            
            if is_break:
                continue
            
            # Regular period
            period = self._create_regular_period(current_time, day)
            if period:
                periods.append(period)
                current_time = period.end_time
            else:
                # If we couldn't create a period, move to next slot
                current_time = self._add_minutes(current_time, PERIOD_DURATION.seconds // 60)
        
        return periods
    
    def _create_regular_period(
        self,
        start_time: time,
        day: str
    ) -> Optional[Period]:
        """Create a regular teaching period."""
        end_time = self._add_minutes(start_time, PERIOD_DURATION.seconds // 60)
        
        # Try subjects that still need to be allocated
        subjects_to_try = sorted(
            [
                (subject, remaining)
                for subject, remaining in self.remaining_periods.items()
                if remaining > 0
            ],
            key=lambda x: (-x[1], x[0])  # Sort by remaining count (desc) then subject name
        )
        
        # If no subjects need allocation, return None
        if not subjects_to_try:
            return None
        
        # Try each subject
        for subject, _ in subjects_to_try:
            # Find available teacher
            for teacher in self.teachers:
                if (teacher.can_teach_subject(subject) and
                    teacher.is_available(day, start_time, end_time)):
                    # Create period and update remaining count
                    self.remaining_periods[subject] -= 1
                    return Period(
                        start_time=start_time,
                        end_time=end_time,
                        subject=subject,
                        teacher=teacher.name
                    )
        
        # No teacher available for any remaining subject
        return None
    
    @staticmethod
    def _add_minutes(t: time, minutes: int) -> time:
        """Add minutes to a time object."""
        minutes_since_midnight = t.hour * 60 + t.minute + minutes
        return time(minutes_since_midnight // 60, minutes_since_midnight % 60)
    
    @staticmethod
    def _time_equals(t1: time, t2: time) -> bool:
        """Compare two time objects."""
        return t1.hour == t2.hour and t1.minute == t2.minute
    
    def export_to_excel(self, filename: str) -> None:
        """Export the timetable to an Excel file."""
        data = []
        for day in WORKING_DAYS:
            for period in self.timetable[day]:
                data.append({
                    'Day': day,
                    'Start Time': period.start_time.strftime('%I:%M %p'),
                    'End Time': period.end_time.strftime('%I:%M %p'),
                    'Subject': period.subject,
                    'Teacher': period.teacher if period.teacher else 'N/A'
                })
        
        df = pd.DataFrame(data)
        df.drop_duplicates(inplace=True)
        df.to_excel(filename, index=False, engine='openpyxl')
