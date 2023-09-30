from app.api import bp
from app.extensions import db
from flask import current_app, render_template, json, request
from flask_login import login_required, current_user
from app.models import Media
from app.scripts.media import delete_media_everywhere

@bp.route("/medias/<int:media_id>/picks_modal", methods=['GET'])
@login_required
def picks_modal(media_id):
    media = Media.query.get_or_404(media_id)
    content = render_template("views/picks_modal.html", media=media)
    return content

@bp.route("/medias/<int:media_id>/delete", methods=['DELETE'])
@login_required
def delete_media(media_id):
    if not current_user.admin:
        return {
            "error" : "Not allowed!"
        }, 405
    media = Media.query.get_or_404(media_id)
    current_app.logger.debug(str(current_user)+" is trying to delete "+str(media))
    script_result = delete_media_everywhere(media)
    return {
        "message" : script_result
    }

@bp.route("/medias", methods=['GET'])
def get_medias():
    query = Media.query
    total = query.count()

    # Filtering for selected media types
    media_type_search = request.args.get('media_types').split(',')
    query = query.filter(
        Media.type.in_(media_type_search)
    )
    total = query.count()

    # Search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Media.title.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # Sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name == 'title':  # Sorting by Title column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Media.title
            if descending:
                col = col.desc()
            order.append(col)
        if col_name == 'media_size':  # Sorting by Size column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Media.total_size
            if descending:
                col = col.desc()
            order.append(col)
        if col_name == 'deletion_date':  # Sorting by Deletion Date column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Media.deletion_date
            if descending:
                col = col.desc()
            order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # Pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # Response
    return {
        'data': [media.to_dict() for media in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total,
        'draw': request.args.get('draw', type=int),
    }