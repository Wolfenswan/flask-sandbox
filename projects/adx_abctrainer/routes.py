from flask import Blueprint, render_template, redirect, url_for

from projects.adx_abctrainer.adx_abctrainer import parse_word_to_html, WORD_LIST
from projects.adx_abctrainer.form import InputForm

adx_abctrainer_bp = Blueprint('adx_abctrainer', __name__, template_folder='templates/adx_abctrainer/')

@adx_abctrainer_bp.route('/', subdomain='abctrainer')
def abctrainer_subdomain():
    return redirect(url_for('.abctrainer_form'))

@adx_abctrainer_bp.route('/adx_abctrainer/', methods=["GET", "POST"])
def abctrainer_form():
    form = InputForm()
    if form.validate_on_submit():
        return redirect('/adx_abctrainer/'+form.word.data)
    return render_template("adx_abctrainer/form.html", form=form, word_list = WORD_LIST)


@adx_abctrainer_bp.route('/adx_abctrainer/<word>')
def abctrainer_word(word):
    if word.isalpha() and len(word) <= 18:
        word = parse_word_to_html(word)
        return render_template('adx_abctrainer/word.html', word=word)
    else:
        return redirect('/adx_abctrainer/')
