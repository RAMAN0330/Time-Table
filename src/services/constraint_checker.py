from typing import Dict, List, Set
from ..models.period import Period
from ..config import MIN_PERIODS_PER_DAY, MAX_PERIODS_PER_DAY, WORKING_DAYS

class ConstraintChecker:
    def __init__(self, timetable: Dict[str, List[Period]]):
        self.timetable = timetable
    
    def check_all_constraints(self) -> List[str]:
        """Check all timetable constraints and return list of violations."""
        violations = []
        violations.extend(self.check_period_count())
        violations.extend(self.check_teacher_conflicts())
        violations.extend(self.check_subject_distribution())
        return violations
    
    def check_period_count(self) -> List[str]:
        """Check if each day has the correct number of periods."""
        violations = []
        for day in WORKING_DAYS:
            regular_periods = [p for p in self.timetable[day] 
                             if not (p.is_break or p.is_assembly)]
            count = len(regular_periods)
            
            if count < MIN_PERIODS_PER_DAY:
                violations.append(
                    f"{day} has only {count} periods, minimum required is {MIN_PERIODS_PER_DAY}"
                )
            elif count > MAX_PERIODS_PER_DAY:
                violations.append(
                    f"{day} has {count} periods, maximum allowed is {MAX_PERIODS_PER_DAY}"
                )
        return violations
    
    def check_teacher_conflicts(self) -> List[str]:
        """Check if any teacher is scheduled for multiple classes at the same time."""
        violations = []
        for day in WORKING_DAYS:
            teacher_schedules: Dict[str, List[Period]] = {}
            
            for period in self.timetable[day]:
                if period.teacher:
                    if period.teacher not in teacher_schedules:
                        teacher_schedules[period.teacher] = []
                    teacher_schedules[period.teacher].append(period)
            
            # Check for overlapping periods
            for teacher, periods in teacher_schedules.items():
                for i, p1 in enumerate(periods):
                    for p2 in periods[i+1:]:
                        if (p1.start_time <= p2.start_time < p1.end_time or
                            p2.start_time <= p1.start_time < p2.end_time):
                            violations.append(
                                f"Teacher {teacher} has conflicting periods on {day} "
                                f"at {p1.start_time}-{p1.end_time} and {p2.start_time}-{p2.end_time}"
                            )
        return violations
    
    def check_subject_distribution(self) -> List[str]:
        """Check if subjects are well-distributed throughout the week."""
        violations = []
        subject_counts: Dict[str, int] = {}
        
        # Count subjects
        for day in WORKING_DAYS:
            for period in self.timetable[day]:
                if not (period.is_break or period.is_assembly):
                    subject_counts[period.subject] = subject_counts.get(period.subject, 0) + 1
        
        # Check for subjects that appear too frequently or rarely
        total_periods = sum(subject_counts.values())
        for subject, count in subject_counts.items():
            if count > total_periods * 0.3:  # No subject should take up more than 30% of periods
                violations.append(
                    f"Subject {subject} appears too frequently ({count} times)"
                )
            elif count < 2:  # Each subject should appear at least twice per week
                violations.append(
                    f"Subject {subject} appears too rarely ({count} times)"
                )
        
        return violations
