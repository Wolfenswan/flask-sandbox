import random
from pathlib import Path

from flask import Blueprint, render_template, redirect, url_for, request, Flask, flash

from projects.adx_abctrainer.adx_abctrainer import parse_word, WORDS_RANDOM, WORDS_PRESELECTED, WORD_LENGTH_MIN, \
    WORD_LENGTH_MAX, INSTANCE_PATH
from projects.adx_abctrainer.form import InputForm, RandomForm, AddWordForm

adx_abctrainer_bp = Blueprint('adx_abctrainer', __name__, template_folder='templates/adx_abctrainer/')

@adx_abctrainer_bp.route('/', subdomain='abctrainer')
def abctrainer_subdomain():
    return redirect(url_for('.abctrainer_form'))

@adx_abctrainer_bp.route('/adx_abctrainer/', methods=["GET", "POST"])
def abctrainer_form():
    form = InputForm()
    form_2 = RandomForm()
    if form.validate_on_submit() and form.submit.data:
        return redirect(url_for('.abctrainer_word', word = form.word.data))
    elif form_2.validate_on_submit() and form_2.submit.data:
        #return redirect('/adx_abctrainer/random',min=3,max=22)
        return redirect(url_for('.abctrainer_random', min=form_2.min.data,max=form_2.max.data))
    return render_template("adx_abctrainer/form.html", form=form, form_2 = form_2, word_list = WORDS_PRESELECTED, min=WORD_LENGTH_MIN, max=WORD_LENGTH_MAX)

@adx_abctrainer_bp.route('/adx_abctrainer/<word>', methods=["GET", "POST"])
def abctrainer_word(word):

    form_2 = RandomForm()
    min_length = int(request.args.get('min', WORD_LENGTH_MIN))
    max_length = int(request.args.get('max', WORD_LENGTH_MAX))

    if form_2.validate_on_submit() and form_2.submit.data:
        return redirect(f'/adx_abctrainer/random?min={form_2.min.data}&max={form_2.max.data}')

    if word.isalpha() and len(word) >= WORD_LENGTH_MIN and len(word) <= WORD_LENGTH_MAX:
        word = parse_word(word)
        return render_template('adx_abctrainer/word.html', word=word, form_2 = form_2, randomize=False, min=min_length, max=max_length, min_abs=WORD_LENGTH_MIN, max_abs = WORD_LENGTH_MAX)
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
        #return redirect(f'/adx_abctrainer/{word}?min={min_length}&max={max_length}')
        return redirect(url_for('.abctrainer_word', word = word, min=min_length, max=max_length))
    return redirect('/adx_abctrainer/')

@adx_abctrainer_bp.route('/adx_abctrainer/neues_wort', methods=["GET", "POST"])
def abctrainer_new():
    form = AddWordForm()

    if form.validate_on_submit():
        new_word = form.word.data

        # add new word or delete if already contained in lists
        WORDS_PRESELECTED.append(new_word) if not new_word in WORDS_PRESELECTED else WORDS_PRESELECTED.remove(new_word)
        WORDS_RANDOM.append(new_word) if not new_word in WORDS_RANDOM else WORDS_RANDOM.remove(new_word)

        # overwrite txt with pre-selected files according to new list
        with open(Path(f'{INSTANCE_PATH}/woerter_vorauswahl.txt'), 'w') as f:
            for word in WORDS_PRESELECTED:
                f.write(f'{word}\n')

        return redirect('/adx_abctrainer/neues_wort')

    return render_template("adx_abctrainer/form.html", form=form, form_2=None, word_list=WORDS_PRESELECTED, min=WORD_LENGTH_MIN, max=WORD_LENGTH_MAX)
