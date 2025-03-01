from flask import Blueprint, redirect, url_for
from flask_login import login_required
from models.device import Device

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
@home_bp.route('/index', methods=['GET'])
@login_required
def index ():
    return redirect(url_for("device.index"))