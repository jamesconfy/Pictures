from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
    img = FileField('Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')