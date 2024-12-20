from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired
import os
from datetime import datetime

from models.class_info import ClassInfo
from models.teacher import Teacher
from services.timetable_generator import TimetableGenerator
from utils.helpers import load_teacher_data, parse_time
from config import CLASSES, DIVISIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class TimetableForm(FlaskForm):
    class_name = SelectField('Class', choices=[(c, c) for c in CLASSES], validators=[DataRequired()])
    division = SelectField('Division', choices=[(d, d) for d in DIVISIONS], validators=[DataRequired()])
    teacher_file = StringField('Teacher Data File Path', validators=[DataRequired()])
    submit = SubmitField('Generate Timetable')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TimetableForm()
    if form.validate_on_submit():
        try:
            # Load teacher data
            teachers = load_teacher_data(form.teacher_file.data)
            
            # Create class info
            class_info = ClassInfo(
                name=form.class_name.data,
                division=form.division.data,
                start_time=parse_time("8:15 AM"),
                end_time=parse_time("2:15 PM"),
                breaks=[(parse_time("12:45 PM"), parse_time("1:15 PM"))]
            )
            
            # Generate timetable
            generator = TimetableGenerator(
                class_info=class_info,
                teachers=[Teacher(**t) for t in teachers],
                subject_distribution={"Mathematics": 6, "Science": 4, "English": 6, "Social Studies": 4}
            )
            
            timetable = generator.generate_timetable()
            
            # Export to Excel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"timetable_{class_info.class_name}_{timestamp}.xlsx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            generator.export_to_excel(filepath)
            
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            flash(f"Error generating timetable: {str(e)}", 'error')
            return redirect(url_for('index'))
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
