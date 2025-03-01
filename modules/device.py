from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models.device import Device
from models.user import Role
from forms.device.DeviceForm import DeviceForm
from db.db import db

device_bp = Blueprint('device', __name__)

@device_bp.route('/', methods=['GET'])
@device_bp.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.role.name in ['Teacher', 'Admin']:
        devices = Device.query.all()
    else:
        devices = Device.query.filter_by(is_available=True).all()
    return render_template('index.html', devices=devices)

@device_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DeviceForm()
    if form.validate_on_submit():
        new_device = Device(
            device_name=form.device_name.data,
            device_type=form.device_type.data,
            description=form.description.data,
            is_available=form.is_available.data
        )
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for('device.index'))
    return render_template('device/add.html', form=form)

@device_bp.route('/edit/<int:device_id>', methods=['GET', 'POST'])
@login_required
def edit(device_id):
    device = Device.query.get_or_404(device_id)
    form = DeviceForm(obj=device)
    if form.validate_on_submit():
        form.populate_obj(device)
        db.session.commit()
        return redirect(url_for('device.index'))
    return render_template('device/edit.html', form=form, device=device)

@device_bp.route('/delete/<int:device_id>', methods=['POST'])
@login_required
def delete(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('device.index'))

@device_bp.route('/reserve/<int:device_id>', methods=['POST'])
@login_required
def reserve(device_id):
    device = Device.query.get_or_404(device_id)
    if device.is_available:
        device.is_available = False
        device.user_id = current_user.id
        db.session.commit()
    return redirect(url_for('device.index'))

@device_bp.route('/unreserve/<int:device_id>', methods=['POST'])
@login_required
def unreserve(device_id):
    device = Device.query.get_or_404(device_id)
    if current_user.role in [Role.Teacher, Role.Admin] and not device.is_available:
        device.is_available = True
        device.user_id = None
        db.session.commit()
    return redirect(url_for('device.index'))