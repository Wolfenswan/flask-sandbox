# future:
# https://pypi.org/project/xhtml2pdf/ OR https://pypi.org/project/imgkit/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask

from markupsafe import Markup

def parse_word_to_html(word):
    html_list = ['<div>']
    image_folder = '/static/adx_abctrainer/images/'
    for i, letter in enumerate(list(word)):
        path = f'{image_folder}/{letter.lower()}.png'
        img = f'{path}'
        html = f'<img src={img}>'
        html_list.append(html)
        if (i + 1) % 6 == 0:
            html_list.append('</div>\n<div>')
    html_list.append('</div>')
    finalized_html = [Markup(tag) for tag in html_list]
    return finalized_html