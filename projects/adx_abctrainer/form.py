from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class InputForm(FlaskForm):
    word = StringField('Zauberwort eingeben:', validators=[DataRequired(message='Gib was ein!'),Length(max=22, message='Maximal 18 Buchstaben!')])
    submit = SubmitField('Spuck was aus!')

    def validate_word(form, field):
        illegal_characters = ['ß','ä','ö','ü']
        if not field.data.isalpha() or sum([char in field.data for char in illegal_characters])>0:
            raise ValidationError("Nur Buchstaben von A-Z erlaubt!")