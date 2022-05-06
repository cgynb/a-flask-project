from flask import Blueprint, render_template, jsonify, request
from require import admin_required
from models import NoticeModel
from exts import db

bp = Blueprint('admin', __name__, url_prefix='/admin/')


@bp.route('/')
@admin_required
def charge():
    return render_template('admin/charge.html')

