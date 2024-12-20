import pytest
from datetime import time
from src.models.class_info import ClassInfo
from src.models.teacher import Teacher
from src.models.period import Period
from src.services.timetable_generator import TimetableGenerator
from src.services.constraint_checker import ConstraintChecker

@pytest.fixture
def sample_class_info():
    return ClassInfo(
        name="1st",
        division="A",
        start_time=time(8, 15),
        end_time=time(14, 15),
        breaks=[
            (time(9, 25), time(9, 45)),
            (time(12, 45), time(13, 15))
        ]
    )

@pytest.fixture
def sample_teachers():
    return [
        Teacher(
            name="John Doe",
            subjects=["Mathematics", "Science"],
            classes=["1st"],
            availability={
                "Monday": [(time(8, 15), time(14, 15))],
                "Tuesday": [(time(8, 15), time(14, 15))],
                "Wednesday": [(time(8, 15), time(14, 15))],
                "Thursday": [(time(8, 15), time(14, 15))],
                "Friday": [(time(8, 15), time(14, 15))]
            }
        ),
        Teacher(
            name="Jane Smith",
            subjects=["English", "Social Studies"],
            classes=["1st"],
            availability={
                "Monday": [(time(8, 15), time(14, 15))],
                "Tuesday": [(time(8, 15), time(14, 15))],
                "Wednesday": [(time(8, 15), time(14, 15))],
                "Thursday": [(time(8, 15), time(14, 15))],
                "Friday": [(time(8, 15), time(14, 15))]
            }
        )
    ]

@pytest.fixture
def subject_distribution():
    return {
        "Mathematics": 6,
        "Science": 4,
        "English": 6,
        "Social Studies": 4
    }

def test_timetable_generation(sample_class_info, sample_teachers, subject_distribution):
    generator = TimetableGenerator(
        class_info=sample_class_info,
        teachers=sample_teachers,
        subject_distribution=subject_distribution
    )
    
    timetable = generator.generate_timetable()
    
    # Basic validation
    assert timetable is not None
    assert len(timetable) == 5  # 5 working days
    
    # Check constraints
    checker = ConstraintChecker(timetable)
    violations = checker.check_all_constraints()
    
    # Print violations for debugging
    for violation in violations:
        print(f"Constraint violation: {violation}")
    
    assert len(violations) == 0, "Timetable should not have any constraint violations"

def test_period_creation(sample_class_info, sample_teachers, subject_distribution):
    generator = TimetableGenerator(
        class_info=sample_class_info,
        teachers=sample_teachers,
        subject_distribution=subject_distribution
    )
    
    # Test regular period creation
    period = generator._create_regular_period(time(8, 15), "Monday")
    assert period is not None
    assert isinstance(period, Period)
    assert period.start_time == time(8, 15)
    assert period.end_time == time(8, 45)
    assert period.teacher in [t.name for t in sample_teachers]
    assert period.subject in subject_distribution.keys()

def test_class_info_methods(sample_class_info):
    # Test class name formatting
    assert sample_class_info.class_name == "1st-A"
    
    # Test break time checking
    assert sample_class_info.is_break_time(time(9, 30))  # During first break
    assert sample_class_info.is_break_time(time(13, 0))  # During lunch break
    assert not sample_class_info.is_break_time(time(10, 0))  # Not during break
