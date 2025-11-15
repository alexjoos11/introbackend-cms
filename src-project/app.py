from db import db  # you may also import your models here, e.g. Course, User, Assignment
from flask import Flask, request, jsonify

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# =========================
#        COURSES
# =========================

@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    GET /api/courses/
    Returns:
        200: {
            "courses": [
                {
                    "id": ...,
                    "code": ...,
                    "name": ...,
                    "assignments": [ <SERIALIZED ASSIGNMENT W/O COURSE FIELD>, ... ],
                    "instructors": [ <SERIALIZED USER W/O COURSES FIELD>, ... ],
                    "students": [ <SERIALIZED USER W/O COURSES FIELD>, ... ]
                },
                ...
            ]
        }
    """
    # TODO: query all courses, serialize them (omitting nested course/courses fields)
    return jsonify({"courses": []}), 200


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    POST /api/courses/
    Request JSON:
        {
            "code": "<course code>",
            "name": "<course name>"
        }
    Returns:
        201 with serialized course on success:
            {
                "id": <ID>,
                "code": ...,
                "name": ...,
                "assignments": [],
                "instructors": [],
                "students": []
            }
        400 if code or name missing.
    """
    body = request.get_json()
    # TODO: validate body, create & commit Course, return serialized course
    return jsonify({"error": "not implemented"}), 501


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    """
    GET /api/courses/{id}/
    Returns:
        200 with serialized course:
            {
                "id": <ID>,
                "code": ...,
                "name": ...,
                "assignments": [ <SERIALIZED ASSIGNMENT W/O COURSE FIELD>, ... ],
                "instructors": [ <SERIALIZED USER W/O COURSES FIELD>, ... ],
                "students": [ <SERIALIZED USER W/O COURSES FIELD>, ... ]
            }
        404 if course not found.
    """
    # TODO: lookup course by id, serialize, handle 404
    return jsonify({"error": "not implemented"}), 501


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    DELETE /api/courses/{id}/
    Returns:
        200 with serialized deleted course (same shape as GET /api/courses/{id}/)
        404 if course not found.
    """
    # TODO: lookup course, delete it, return serialized deleted course
    return jsonify({"error": "not implemented"}), 501


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    POST /api/courses/{id}/add/
    Request JSON:
        {
            "user_id": <USER ID>,
            "type": "student" or "instructor"
        }
    Returns:
        200 with serialized course (same shape as GET /api/courses/{id}/)
        including the newly added user in the appropriate list.
        400 if type invalid or body missing fields.
        404 if course or user not found.
    """
    body = request.get_json()
    # TODO: validate body, lookup course and user, add relationship, commit, serialize
    return jsonify({"error": "not implemented"}), 501


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    POST /api/courses/{id}/assignment/
    Request JSON:
        {
            "title": "<title>",
            "due_date": <unix timestamp>
        }
    Returns:
        201:
            {
                "id": <ASSIGNMENT ID>,
                "title": ...,
                "due_date": ...,
                "course": {
                    "id": <course_id>,
                    "code": ...,
                    "name": ...
                }
            }
        400 if title or due_date missing.
        404 if course not found.
    """
    body = request.get_json()
    # TODO: validate body, lookup course, create Assignment, commit, serialize
    return jsonify({"error": "not implemented"}), 501


# =========================
#          USERS
# =========================

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    POST /api/users/
    Request JSON:
        {
            "name": "<user name>",
            "netid": "<netid>"
        }
    Returns:
        201:
            {
                "id": <ID>,
                "name": ...,
                "netid": ...,
                "courses": []
            }
        400 if name or netid missing.
    """
    body = request.get_json()
    # TODO: validate body, create & commit User, serialize response
    return jsonify({"error": "not implemented"}), 501


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    GET /api/users/{id}/
    Returns:
        200:
            {
                "id": <ID>,
                "name": ...,
                "netid": ...,
                "courses": [
                    <SERIALIZED COURSE W/O assignments/students/instructors>, ...
                ]
            }
        404 if user not found.
    Note: courses should include *all* courses where the user is a student or instructor.
    """
    # TODO: lookup user, gather all courses (student + instructor), serialize
    return jsonify({"error": "not implemented"}), 501


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
