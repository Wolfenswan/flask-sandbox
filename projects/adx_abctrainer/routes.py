import random

from flask import Blueprint, render_template, redirect, url_for, request

from projects.adx_abctrainer.adx_abctrainer import parse_word, WORDS_RANDOM, WORDS_PRESELECTED, WORD_LENGTH_MIN, \
    WORD_LENGTH_MAX
from projects.adx_abctrainer.form import InputForm, RandomForm

adx_abctrainer_bp = Blueprint('adx_abctrainer', __name__, template_folder='templates/adx_abctrainer/')

@adx_abctrainer_bp.route('/', subdomain='abctrainer')
def abctrainer_subdomain():
    return redirect(url_for('.abctrainer_form'))

@adx_abctrainer_bp.route('/adx_abctrainer/', methods=["GET", "POST"])
def abctrainer_form():
    form = InputForm()
    form_2 = RandomForm()
    if form.validate_on_submit() and form.submit.data:
        return redirect(f'/adx_abctrainer/{form.word.data}')
    elif form_2.validate_on_submit() and form_2.submit.data:
        #return redirect('/adx_abctrainer/random',min=3,max=22)
        return redirect(f'/adx_abctrainer/random?min={form_2.min.data}&max={form_2.max.data}')
    return render_template("adx_abctrainer/form.html", form=form, form_2 = form_2, word_list = WORDS_PRESELECTED, min=WORD_LENGTH_MIN, max=WORD_LENGTH_MAX)

@adx_abctrainer_bp.route('/adx_abctrainer/<word>', methods=["GET", "POST"])
def abctrainer_word(word):

    form_2 = RandomForm()
    min = int(request.args.get('min', WORD_LENGTH_MIN))
    max = int(request.args.get('max', WORD_LENGTH_MAX))

    if form_2.validate_on_submit() and form_2.submit.data:
        return redirect(f'/adx_abctrainer/random?min={form_2.min.data}&max={form_2.max.data}')

    if word.isalpha() and len(word) >= WORD_LENGTH_MIN and len(word) <= WORD_LENGTH_MAX:
        word = parse_word(word)
        return render_template('adx_abctrainer/word.html', word=word, form_2 = form_2, randomize=False, min=min, max=max)
    else:
        return redirect('/adx_abctrainer/')

@adx_abctrainer_bp.route('/adx_abctrainer/random')
def abctrainer_random():
    min_length = int(request.args.get('min',WORD_LENGTH_MIN))
    max_length = int(request.args.get('max',WORD_LENGTH_MAX))

    possible_words = [word for word in WORDS_RANDOM if len(word) >= min_length and len(word) <= max_length]
    if len(possible_words) > 0:
        word = random.choice(possible_words)
    else: # fallback in case no word of the selected length is in the list
        word = max(WORDS_RANDOM, key=len)

    if word != '':
        return redirect(f'/adx_abctrainer/{word}?min={min}&max={max}')
    return redirect('/adx_abctrainer/')
