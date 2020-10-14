# future:
# https://pypi.org/project/xhtml2pdf/ OR https://pypi.org/project/imgkit/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
from pathlib import Path

from flask import url_for
from markupsafe import Markup

def parse_word_to_html(word):
    html_list = ['<div>']
    for i, letter in enumerate(list(word)):
        img_path = url_for('static', filename=f'adx_abctrainer/img/{letter.lower()}.png')
        html = f'<img src="{img_path}">'
        html_list.append(html)
        if (i + 1) % 6 == 0:
            html_list.append('</div>\n<div>')
    html_list.append('</div>')
    finalized_html = [Markup(tag) for tag in html_list]
    return finalized_html