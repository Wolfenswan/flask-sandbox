from projects.adx_wodzefack import adx_wodzefack
from flask import Blueprint, render_template, redirect, url_for, request, Flask, flash
from datetime import date, datetime

adx_wodzefack_bp = Blueprint('adx_wodzefack', __name__, template_folder='templates/adx_wodzefack/')


@adx_wodzefack_bp.route('/wod/', methods=["GET"])
def wod():
    today = date.today()
    return render_template("adx_wodzefack/wod.html", today=today.strftime("%d.%m.%Y") ,workout = adx_wodzefack.get_workout(today))

@adx_wodzefack_bp.route('/wod/<day>.<month>', methods=["GET"])
def wod_specific(day, month):
    today = datetime.strptime(f'{day}.{month}.2021', '%d.%m.%Y')
    return render_template("adx_wodzefack/wod.html", today=today.strftime("%d.%m.%Y") ,workout = adx_wodzefack.get_workout(today))