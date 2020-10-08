from pathlib import Path

from flask import Flask

class Constants():
    ROOT = Flask(__name__).root_path
    TEMPLATE_PDF = Path(f'{ROOT}/vorlagen/bestellschein.pdf')
    OUTPUT_FOLDER = Path(f'{ROOT}/output/')
    # TEMPLATE_PDF = Path('static/vorlagen/bestellschein.pdf')
    # OUTPUT_FOLDER = Path(f'static/output')
    QUERY_URL = 'https://recherche.staatsarchiv.hamburg.de/ScopeQuery5.2/detail.aspx?ID='

    NAME_KEY = "Name"
    DATE_KEY = "Datum"
    ID1_KEY = "Bestand"
    ID2_KEY = "Sig"