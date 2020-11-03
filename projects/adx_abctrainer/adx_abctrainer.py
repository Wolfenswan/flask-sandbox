# future:
# https://pypi.org/project/xhtml2pdf/ OR https://pypi.org/project/imgkit/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
from pathlib import Path

from flask import url_for, Flask
from markupsafe import Markup

WORD_LENGTH_MIN = 3
WORD_LENGTH_MAX = 18

with open(Path(f'{Flask(__name__).root_path}/static/woerter_vorauswahl.txt'), 'r') as f:
    WORDS_PRESELECTED = f.read().split()

with open(Path(f'{Flask(__name__).root_path}/static/woerter_zufall.txt'), 'r') as f:
    WORDS_RANDOM = f.read().split()
    WORDS_RANDOM.append(WORDS_PRESELECTED)

def parse_word_to_html(word):
    """ OBSOLETE Turns the given word into a list of img & div tags for the jinja-template """
    html_list = ['<div class="adx-letters_row">']
    for i, letter in enumerate(list(word)):
        img_path = url_for('static', filename=f'adx_abctrainer/img/abc/{letter.lower()}.png')
        html = f'<img src="{img_path}" class="adx-letter">'
        html_list.append(html)
        if (i + 1) % 6 == 0: # add a new row for each six images
            html_list.append('</div>\n<div class="adx_letters_row">')
    html_list.append('</div>')
    finalized_html = [Markup(tag) for tag in html_list]
    return finalized_html

def parse_word(word):
    """ Returns: list of strings (paths to image for each letter) """
    letters = []
    for letter in list(word):
        img_path = url_for('static', filename=f'adx_abctrainer/img/abc/{letter.lower()}.png')
        letters.append(img_path)
    return letters

