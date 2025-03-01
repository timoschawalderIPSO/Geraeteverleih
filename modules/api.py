from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from models.user import User
from models.device import Device
from db.db import db

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid email or password"}), 401

@api_bp.route('/devices', methods=['GET'])
@jwt_required()
def get_devices():
    user_email = get_jwt_identity()
    user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
    if user.role.name in ['Teacher', 'Admin']:
        devices = Device.query.all()
    else:
        devices = Device.query.filter_by(is_available=True).all()
    return jsonify([device.to_dict() for device in devices]), 200

@api_bp.route('/devices/<int:device_id>/reserve', methods=['POST'])
@jwt_required()
def reserve_device(device_id):
    user_email = get_jwt_identity()
    user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
    device = Device.query.get_or_404(device_id)
    if device.is_available:
        device.is_available = False
        device.user_id = user.id
        db.session.commit()
        return jsonify({"msg": "Device reserved"}), 200
    return jsonify({"msg": "Device not available"}), 400

@api_bp.route('/devices/<int:device_id>/unreserve', methods=['POST'])
@jwt_required()
def unreserve_device(device_id):
    user_email = get_jwt_identity()
    user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar_one_or_none()
    device = Device.query.get_or_404(device_id)
    if user.role.name in ['Teacher', 'Admin'] and not device.is_available:
        device.is_available = True
        device.user_id = None
        db.session.commit()
        return jsonify({"msg": "Device unreserved"}), 200
    return jsonify({"msg": "Unauthorized"}), 403
