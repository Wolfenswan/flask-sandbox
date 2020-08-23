import os
import shutil
import sys

from flask import flash, send_from_directory, Flask, send_file, request
from markupsafe import Markup

from projects.higo_starbesger.starbesger import parse_signatures, parse_urls, write_order_pdf, process_form_data, \
    create_zip, stream_zip
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

        if not Constants.OUTPUT_FOLDER.exists():
            Path.mkdir(Constants.OUTPUT_FOLDER)

        order_folder = Path(f"{Constants.OUTPUT_FOLDER}/{name}_{datum}")
        if not order_folder.exists():
            Path.mkdir(order_folder)
        flash(f'Schreibe in ordner {order_folder}!')

        for sig in structured_sigs:
            data = {Constants.NAME_KEY:name, Constants.DATE_KEY: datum, Constants.ID1_KEY:sig[0], Constants.ID2_KEY:sig[1]}
            pdf_name = write_order_pdf(order_folder, data)
            flash(f'"{pdf_name}.pdf" geschrieben')

        #if form.zip_file.data:
        # create ZIP and prepare download
        zip_path = Path(f'{order_folder}/{name}_{datum}.zip')
        create_zip(zip_path, order_folder)
        dl_url = Path(f'/higo_starbesger/output/{name}_{datum}/{name}_{datum}.zip') # dl url needs to be provide a relative path
        message = Markup(f"<a href='{dl_url}?del={form.delete_after_dl.data}&leg={form.legacy_dl.data}'>ZIP herunterladen</a>")
        flash(message)

    return render_template("higo_starbesger/form.html", form=form)

@higo_starbgesger.route('/higo_starbesger/output/<string:folder>/<path:zip>')
def download_file(folder,zip):
    cleanup = request.args.get('del')
    legacy = request.args.get('leg')
    folder_path = Path(f'{Constants.OUTPUT_FOLDER}/{folder}')
    zip_path = Path(f'{folder_path}/{zip}')
    print(f'{cleanup, legacy}', file=sys.stdout)
    if legacy == 'True': # legacy method simply sends the file and keeps all files on the server
        return send_from_directory(folder_path, zip, as_attachment=True)
    else: # stream from memory
        stream_data = stream_zip(zip_path)
        if cleanup == 'True': # cleanup does not work with legacy method
            shutil.rmtree(folder_path)
        return send_file(stream_data, mimetype='application/zip', as_attachment=True, attachment_filename=zip)

