import json

from db import db, Course, User, Assignment
from flask import Flask, request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

#get one course and see if it exists helper
def single_found_check(id, model, name):
    single = model.query.filter_by(id=id).first()
    if single is None:
        return failure_response(name + " not found")
    return single

# =========================
#        COURSES
# =========================

@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    Endpoint for getting all courses
    """
    return success_response({"courses":[t.serialize() for t in Course.query.all()]})


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a new course
    """
    body = json.loads(request.data)
    new_course = Course(code=body.get("code"), name=body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course_by_id(course_id):
    """
    Endpoint for getting a course by id
    """
    course = single_found_check(course_id, Course, "course")
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for delteing a course by id
    """
    course = single_found_check(course_id, Course, "course")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    new_user = User(name=body.get("name"),netid=body.get("netid"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user_by_id(user_id):
    """
    Endpoint fo getting a user by id
    """
    user = single_found_check(user_id, User, "user")
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a user to a course by id
    """
    course = single_found_check(course_id)
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")
    if user_id is None:
        return failure_response("user not found")
    if type == "student": course.students.append(user_id)
    if type == "instructor": course.instructors.append(user_id)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    endpoint for creating an assignment for a course by id
    """
    course = single_found_check(course_id, Course, "course")
    body = json.loads(request.data)
    new_assignment = Assignment(
        title=body.get("title"),
        name=body.get("name"),
        course_id=course_id,
    )
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
