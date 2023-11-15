from app.api import bp
from app.extensions import db
from flask import json, request, current_app
from flask_login import login_required, current_user
from app.models import Media, User, Pick
from app.decorators import super_user_required
from datetime import datetime
from app.scripts.media import check_user_creation, check_movie_creation, check_tv_show_creation, check_pick_creation, delete_pick_and_check_abandoned

@bp.route("/picks/<int:media_id>/add_to_current_user", methods=['PUT'])
@login_required
def add_pick_to_current_user(media_id):
    media = Media.query.get(media_id)
    check_pick_creation(media, current_user, datetime.utcnow(), "Picked up")
    return{
        "message" : f"Picked up {media}"
    }

@bp.route("/picks/<int:media_id>/add_permanent", methods=['PUT'])
@login_required
@super_user_required
def add_pick_permanent_collection(media_id):
    media = Media.query.get(media_id)
    permanent_user = User.query.filter_by(email="Permanent").first()
    check_pick_creation(media, permanent_user, datetime.utcnow(), "Assigned")
    return{
        "message" : f'{media} added to the permanent collection'
    }

@bp.route("/picks/add_watching", methods=['PUT'])
def add_pick_watching():
    data = json.loads((request.data.decode("utf-8")))
    current_app.logger.debug(data["email"]+" started watching something.")
    user, added_user = check_user_creation(data["email"], data["alias"])

    if data["type"] == "movie":
        #Only process if this is an actual movie
        if data["themoviedb_id"]:
            current_app.logger.info(f'{user} started watching movie: {data["title"]}')
            movie, added_movie = check_movie_creation(TMDB_id=data["themoviedb_id"])
            check_pick_creation(movie, user, datetime.utcnow(), "Watched")

    elif data["type"] == "tv_show":
        #Only process if this is an actual show
        if data["thetvdb_id"]:
            current_app.logger.info(f'{user} started watching tv show: {data["show_title"]}')
            tv_show, added_to_db = check_tv_show_creation(theTVDB_id=data["thetvdb_id"])
            check_pick_creation(tv_show, user, datetime.utcnow(), "Watched")
    return {}, 204

@bp.route("/picks/<int:pick_id>/delete", methods=['DELETE'])
@login_required
def delete_pick(pick_id):
    pick = Pick.query.get_or_404(pick_id)
    media = pick.media
    current_app.logger.debug(f'User {current_user.alias} is trying to delete {pick}')
    if (current_user.is_super_user()) or (current_user==pick.user):
        abandoned = delete_pick_and_check_abandoned(pick)
        if abandoned:
            return{
                "message" : f'{media} was let go. It has been abandoned as this was its last pick.'
            }
        else:
            return{
                "message" : f'{media} was let go. Others have picked this media, and it has not been abandoned yet.'
            }
    else:
        return {
            "error" : "Not allowed!"
        }, 405

@bp.route("/picks", methods=['GET'])
@login_required
def get_picks():
    query = Pick.query.outerjoin(Media)

    # Filtering for the specified user
    lookup_user = request.args.get('user')
    if lookup_user == "self":
        query = query.filter(
            Pick.user_id.like(current_user.id)
        )
    else:
        query = query.filter(
             Pick.user_id.like(lookup_user)
        )

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
            Pick.pick_method.like(f'%{search}%'),
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
        if col_name == 'pick_date':  # Sorting by pick_date or pick_method column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Pick.pick_date
            if descending:
                col = col.desc()
            order.append(col)
        elif col_name == 'media_title':  # Sorting by Title column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Media.title
            if descending:
                col = col.desc()
            order.append(col)
        elif col_name == 'media_size':  # Sorting by Size column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Media.total_size
            if descending:
                col = col.desc()
            order.append(col)
        elif col_name == 'pick_method':  # Sorting by Size column
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = Pick.pick_method
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
        'data': [pick.to_dict() for pick in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total,
        'draw': request.args.get('draw', type=int),
    }