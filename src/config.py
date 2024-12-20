from datetime import time, timedelta

# Class configurations
CLASSES = ["Jr.Kg", "Sr.Kg", "1st"]
DIVISIONS = ["A", "B", "C", "D"]

# Time configurations
PERIOD_DURATION = timedelta(minutes=30)
ASSEMBLY_DAY = "Tuesday"
ASSEMBLY_TIME = time(10, 45)
WORKING_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Period constraints
MIN_PERIODS_PER_DAY = 6
MAX_PERIODS_PER_DAY = 8

# Class timings
CLASS_TIMINGS = {
    "Jr.Kg": {"start": time(10, 15), "end": time(14, 15)},
    "Sr.Kg": {"start": time(10, 15), "end": time(14, 15)},
    "1st": {"start": time(8, 15), "end": time(14, 15)},
}

# Break timings
BREAK_TIMINGS = {
    "Jr.Kg": [(time(12, 45), time(13, 15))],  # Lunch break
    "Sr.Kg": [(time(12, 45), time(13, 15))],  # Lunch break
    "1st": [
        (time(9, 25), time(9, 45)),    # Morning break
        (time(12, 45), time(13, 15)),  # Lunch break
    ],
}

# Subject configurations
SUBJECTS = {
    "Jr.Kg": ["English", "Mathematics", "Environmental Science", "Art", "Physical Education"],
    "Sr.Kg": ["English", "Mathematics", "Environmental Science", "Art", "Physical Education"],
    "1st": ["English", "Mathematics", "Science", "Social Studies", "Art", "Physical Education"],
}
