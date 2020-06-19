from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError

def signaturen_validation():
    def _signaturen_validation(form, field):
        if field.data != "":
            signaturen = field.data.split('\r\n')
            for sig in signaturen:
                dash_count = sig.count('_')
                if dash_count > 2:
                    raise ValidationError(f'Signaturen dürfen maximal zwei Unterstriche enthalten! Erste fehlerhafte Signatur: {sig}')
                elif dash_count == 0:
                    raise ValidationError(f'Signaturen müssen mindestens einen Unterstrich enthalten! Erste fehlerhafte Signatur: {sig}')
    return _signaturen_validation

def url_validation():
    def _url_validation(form, field):
        if field.data != "":
            urls = field.data.split('\r\n')
            if len(urls) > 0:
                for url in urls:
                    if not url.isdigit(): #Todo check length variation for search id
                        raise ValidationError(f'Such-IDs dürfen nur Zahlen enthalten! Erste fehlerhafte ID: {url}')
    return _url_validation

class InputForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Bitte Namen des Bestellers angeben')])
    datum = DateField('Datum', validators=[DataRequired(message='Bitte Datum auswählen')])
    signaturen = TextAreaField('Signaturen',[signaturen_validation()])
    urls = TextAreaField('URLs',[url_validation()])
    zip_file = BooleanField('ZIP',description='ZIP-Datei erstellen', default="checked")
    submit = SubmitField('Verarbeiten')

    def validate(self):
        if not super().validate():
            return False
        if self.signaturen.data == "" and self.urls.data == "":
            self.signaturen.errors.append('Bitte Daten in eins oder beide Felder eingeben.')
            self.urls.errors.append('Bitte Daten in eins oder beide Felder eingeben.')
            return False
        return True