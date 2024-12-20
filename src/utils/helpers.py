from datetime import time
from typing import List, Dict, Any
import pandas as pd

def parse_time(time_str: str) -> time:
    """Convert time string to time object."""
    try:
        # If already a time object, return it
        if isinstance(time_str, time):
            return time_str
            
        # Handle 12-hour format with AM/PM
        if 'AM' in time_str.upper() or 'PM' in time_str.upper():
            return pd.to_datetime(time_str).time()
            
        # Handle 24-hour format (HH:MM)
        if ':' in time_str:
            hours, minutes = map(int, time_str.split(':'))
            return time(hours, minutes)
            
        # Handle numeric format (HHMM)
        time_str = str(time_str).zfill(4)
        hours = int(time_str[:2])
        minutes = int(time_str[2:])
        return time(hours, minutes)
            
    except Exception as e:
        raise ValueError(f"Invalid time format: {time_str}") from e

def format_timetable(timetable: Dict[str, List[Any]], format_type: str = 'text') -> str:
    """Format timetable for display/export."""
    if format_type == 'text':
        output = []
        for day, periods in timetable.items():
            output.append(f"\n{day}:")
            for period in periods:
                output.append(f"  {period}")
        return "\n".join(output)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

def validate_input_data(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate input data against required fields."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
