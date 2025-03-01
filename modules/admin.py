from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.user import User, Role
from db.db import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    if current_user.role != Role.Admin:
        return redirect(url_for('device.index'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/promote/<int:user_id>/<role>', methods=['POST'])
@login_required
def promote_user(user_id, role):
    if current_user.role != Role.Admin:
        return redirect(url_for('device.index'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id and role != 'admin':
        return redirect(url_for('admin.list_users'))
    if role == 'admin':
        user.role = Role.Admin
    elif role == 'teacher':
        user.role = Role.Teacher
    elif role == 'student':
        user.role = Role.Student
    db.session.commit()
    return redirect(url_for('admin.list_users'))
