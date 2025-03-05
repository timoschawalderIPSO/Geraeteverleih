from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class DeviceForm(FlaskForm):
    device_name = StringField('Geräte Name', validators=[DataRequired()])
    device_type = StringField('Geräte Typ', validators=[DataRequired()])
    description = StringField('Beschreibung', validators=[DataRequired()])
    is_available = BooleanField('Verfügbar', render_kw={"class": "form-check-input"})
    submit = SubmitField('Bestätigen')
