# School Timetable Management System

A system to generate and manage school timetables for multiple classes and divisions.

## Features

- Support for multiple classes (Jr.Kg, Sr.Kg, 1st)
- Multiple divisions (A, B, C, D)
- Customizable time slots and break periods
- Teacher-subject mapping integration
- Constraint-based timetable generation

## Project Structure

```
.
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── class_info.py
│   │   ├── period.py
│   │   └── teacher.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── timetable_generator.py
│   │   └── constraint_checker.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── tests/
    ├── __init__.py
    └── test_timetable_generator.py
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Unix/macOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

[Usage instructions will be added as the project develops]

## Evaluation Criteria

The project will be evaluated based on:
1. Ability to work with provided data
2. Valid assumptions where necessary
3. Adherence to provided constraints
4. Appropriate teacher-subject assignments
5. Code reproducibility
