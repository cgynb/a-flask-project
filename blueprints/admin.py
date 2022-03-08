from flask import Blueprint, request, redirect, url_for
from decorators import admin_required
from models import CommentModel
from exts import db

bp = Blueprint('admin', __name__, url_prefix='/admin/')


@bp.route('/comment/', methods=['GET'])
@admin_required
def handle_comment():
    food_id = request.args.get('food_id')
    comment_id = request.args.get('comment_id')
    comment = CommentModel.query.filter(CommentModel.id == comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('food.food_details') + f'/?id={food_id}')

