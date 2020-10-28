# future:
# https://pypi.org/project/xhtml2pdf/ OR https://pypi.org/project/imgkit/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
from pathlib import Path

from flask import url_for
from markupsafe import Markup

def parse_word_to_html(word):
    """ Turns the given word into a list of img & div tags for the jinja-template """
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