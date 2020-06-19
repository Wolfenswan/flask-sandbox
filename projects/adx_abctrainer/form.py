from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class InputForm(FlaskForm):
    word = StringField('Zauberwort eingeben:', validators=[DataRequired(message='Gib was ein!'),Length(max=18, message='Maximal 18 Buchstaben!')])
    submit = SubmitField('Spuck was aus!')

    def validate_word(form, field):
        if not field.data.isalpha():
            raise ValidationError("Wörter bestehen üblicherweise nur aus Buchstaben...")