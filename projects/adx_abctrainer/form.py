from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from projects.adx_abctrainer.adx_abctrainer import WORD_LENGTH_MAX, WORD_LENGTH_MIN


class InputForm(FlaskForm):
    word = StringField('Uebungstext', validators=[DataRequired(message='Gib was ein!'),Length(max=WORD_LENGTH_MAX, message=f'Maximal {WORD_LENGTH_MAX} Buchstaben!')])
    submit = SubmitField('Spuck was aus!')

    def validate_word(form, field):
        illegal_characters = ['ß','ä','ö','ü']
        if not field.data.isalpha() or sum([char in field.data for char in illegal_characters])>0:
            raise ValidationError("Nur Buchstaben von A-Z erlaubt!")

class RandomForm(FlaskForm):
    min = DecimalField('Von:', places=1,validators=[NumberRange(min=WORD_LENGTH_MIN, max=WORD_LENGTH_MAX, message=f'Zwischen {WORD_LENGTH_MIN} und {WORD_LENGTH_MAX} Buchstaben sind okay.')])
    max = DecimalField('Bis:', places=1,validators=[NumberRange(min=WORD_LENGTH_MIN, max=WORD_LENGTH_MAX, message=f'Zwischen {WORD_LENGTH_MIN} und {WORD_LENGTH_MAX} Buchstaben sind okay.')])
    submit = SubmitField('Los geht\'s!')