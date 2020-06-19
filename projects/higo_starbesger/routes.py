from flask import flash, send_from_directory, Flask
from markupsafe import Markup

from projects.higo_starbesger.starbesger import parse_signatures, parse_urls, write_order_pdf, process_form_data, create_zip
from projects.higo_starbesger.forms import InputForm
from projects.higo_starbesger.constants import Constants
from pathlib import Path

from flask import Blueprint, render_template
higo_starbgesger = Blueprint('higo_starbgesger', __name__,template_folder='templates/higo_starbesger')

@higo_starbgesger.route('/higo_starbesger/', methods=["GET", "POST"])
def higo_starbesger_form():
    form = InputForm()
    if form.validate_on_submit():
        name, datum, sig_data, url_data = process_form_data(form) # extract strings and lists from submitted form
        flash(f'Daten verarbeitet!')

        if len(url_data) > 0:
            sig_data.extend(parse_urls(url_data))
        structured_sigs = parse_signatures(sig_data)

        order_folder = Path(f"{Constants.OUTPUT_FOLDER}/{name}_{datum}")
        if not order_folder.exists():
            Path.mkdir(order_folder)
        flash(f'Schreibe in ordner {order_folder}!')

        for sig in structured_sigs:
            data = {Constants.NAME_KEY:name, Constants.DATE_KEY: datum, Constants.ID1_KEY:sig[0], Constants.ID2_KEY:sig[1]}
            pdf_name = write_order_pdf(order_folder, data)
            flash(f'"{pdf_name}.pdf" geschrieben')

        if form.zip_file.data:
            zip_path = Path(f'{order_folder}/{name}_{datum}.zip')
            create_zip(zip_path, order_folder)
            dl_url = Path(f'/higo_starbesger/output/{name}_{datum}/{name}_{datum}.zip') # dl url needs to be provide a relative path
            message = Markup(f"<a href='{dl_url}'>ZIP downloaden</a>")
            flash(message)

    return render_template("higo_starbesger/form.html", form=form)


@higo_starbgesger.route('/higo_starbesger/output/<path:filename>')
def download_file(filename):
    return send_from_directory(Constants.OUTPUT_FOLDER, filename, as_attachment=True)
