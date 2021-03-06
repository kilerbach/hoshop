# coding:utf8
"""

Author: ilcwd
"""

import flask


def render_error(error):
    return flask.jsonify({"status": 1, "error": error}), 200


def render_data(data=None):
    return flask.jsonify({"status": 0, "data": data}), 200


def render_dto(dto):
    if dto.ok():
        return render_data(dto.data)

    return render_error(dto.error)


