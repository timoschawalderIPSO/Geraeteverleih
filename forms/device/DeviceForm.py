from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class DeviceForm(FlaskForm):
    device_name = StringField('Device Name', validators=[DataRequired()])
    device_type = StringField('Device Type', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    is_available = BooleanField('Available', render_kw={"class": "form-check-input"})
    submit = SubmitField('Submit')
