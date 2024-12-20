import sys
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time
import json

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.models.class_info import ClassInfo
from src.models.teacher import Teacher
from src.services.timetable_generator import TimetableGenerator
from src.utils.helpers import parse_time
from src.config import CLASSES, DIVISIONS, SUBJECTS, CLASS_TIMINGS, BREAK_TIMINGS

st.set_page_config(
    page_title="School Timetable Generator",
    page_icon="📚",
    layout="wide"
)

def create_timetable_visualization(timetable):
    """Create a Plotly visualization of the timetable"""
    from collections import defaultdict
    
    # First, organize periods by time slots
    time_slots = set()
    day_periods = defaultdict(dict)
    
    for day, periods in timetable.items():
        for period in periods:
            if not (period.is_break or period.is_assembly):
                time_str = f"{period.start_time.strftime('%H:%M')}-{period.end_time.strftime('%H:%M')}"
                time_slots.add(time_str)
                day_periods[day][time_str] = f"{period.subject}<br>({period.teacher})"
    
    # Sort time slots
    time_slots = sorted(list(time_slots))
    
    # Create table data
    table_data = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    # Header row
    header = ["Time"] + days
    
    # Create cells
    cells = []
    cells.append(time_slots)  # First column is time slots
    
    # Add data for each day
    for day in days:
        day_data = []
        for time_slot in time_slots:
            cell_content = day_periods[day].get(time_slot, "")
            day_data.append(cell_content)
        cells.append(day_data)
    
    # Create the table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=header,
            fill_color='paleturquoise',
            align='center',
            font=dict(size=14)
        ),
        cells=dict(
            values=cells,
            fill_color='lavender',
            align='center',
            font=dict(size=12),
            height=40
        )
    )])
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Weekly School Timetable",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        width=1200,
        height=len(time_slots) * 50 + 200
    )
    
    return fig

def load_teacher_data():
    """Create an interactive form for teacher data input"""
    st.sidebar.subheader("👨‍🏫 Teacher Information")
    
    teachers = []
    num_teachers = st.sidebar.number_input("Number of Teachers", min_value=1, max_value=10, value=3)
    
    for i in range(num_teachers):
        with st.sidebar.expander(f"Teacher {i+1}"):
            name = st.text_input(f"Name", key=f"teacher_name_{i}", value=f"Teacher {i+1}")
            subjects = st.multiselect(
                "Subjects",
                ["Mathematics", "Science", "English", "Social Studies", "Art", "Physical Education"],
                key=f"teacher_subjects_{i}"
            )
            classes = st.multiselect(
                "Classes",
                ["1st", "2nd", "3rd", "4th", "5th"],
                key=f"teacher_classes_{i}"
            )
            
            # Time availability
            st.write("Time Availability")
            availability = {}
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            
            for day in days:
                st.write(f"{day}:")
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input(f"Start Time ({day})", key=f"start_{i}_{day}", value=time(9, 0))
                with col2:
                    end_time = st.time_input(f"End Time ({day})", key=f"end_{i}_{day}", value=time(15, 0))
                availability[day] = [[start_time, end_time]]
            
            if subjects and classes:
                teachers.append(Teacher(
                    name=name,
                    subjects=subjects,
                    classes=classes,
                    availability=availability
                ))
    
    return teachers

def main():
    st.title("📚 School Timetable Generator")
    st.sidebar.title("⚙️ Configuration")
    
    # Class selection in sidebar
    st.sidebar.subheader("📝 Class Information")
    selected_class = st.sidebar.selectbox("Select Class", ["1st", "2nd", "3rd", "4th", "5th"])
    selected_division = st.sidebar.selectbox("Select Division", ["A", "B", "C"])
    
    # Class timing in sidebar
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_time = st.time_input("School Start Time", value=time(9, 0))
    with col2:
        end_time = st.time_input("School End Time", value=time(15, 0))
    
    # Break times in sidebar
    st.sidebar.subheader("⏰ Break Times")
    num_breaks = st.sidebar.number_input("Number of Breaks", min_value=0, max_value=3, value=1)
    breaks = []
    
    for i in range(num_breaks):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            break_start = st.time_input(f"Break {i+1} Start", key=f"break_start_{i}", value=time(12, 0))
        with col2:
            break_end = st.time_input(f"Break {i+1} End", key=f"break_end_{i}", value=time(12, 30))
        breaks.append((break_start, break_end))
    
    # Create ClassInfo object
    class_info = ClassInfo(
        name=selected_class,
        division=selected_division,
        start_time=start_time,
        end_time=end_time,
        breaks=breaks
    )
    
    # Get teacher data from sidebar
    teachers = load_teacher_data()
    
    # Subject distribution in sidebar
    st.sidebar.subheader("📚 Subject Distribution")
    subject_distribution = {}
    
    subjects = ["Mathematics", "Science", "English", "Social Studies", "Art", "Physical Education"]
    for subject in subjects:
        periods = st.sidebar.number_input(
            f"{subject} periods/week",
            min_value=0,
            max_value=10,
            value=4,
            key=f"subject_{subject}"
        )
        if periods > 0:
            subject_distribution[subject] = periods
    
    # Generate button in sidebar
    if st.sidebar.button("🎯 Generate Timetable", type="primary"):
        if not teachers:
            st.error("Please add at least one teacher with subjects and classes.")
            return
        
        if not subject_distribution:
            st.error("Please specify at least one subject with periods.")
            return
        
        try:
            with st.spinner("Generating timetable..."):
                # Generate timetable
                generator = TimetableGenerator(
                    class_info=class_info,
                    teachers=teachers,
                    subject_distribution=subject_distribution
                )
                
                timetable = generator.generate_timetable()
                
                if timetable:
                    st.success("✨ Timetable generated successfully!")
                    
                    # Display timetable
                    fig = create_timetable_visualization(timetable)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Export button
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📥 Export to Excel"):
                            filename = f"timetable_{class_info.class_name}.xlsx"
                            generator.export_to_excel(filename)
                            st.success(f"✅ Timetable exported to {filename}")
                else:
                    st.error("❌ Could not generate a valid timetable. Please adjust the constraints.")
                
        except Exception as e:
            st.error(f"❌ Error generating timetable: {str(e)}")

if __name__ == "__main__":
    main()
