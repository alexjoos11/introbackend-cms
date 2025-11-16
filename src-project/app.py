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

# generalized helper formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

#get one course and see if it exists helper
def single_not_found_check(id, model, name):
    single = model.query.filter_by(id=id).first()
    if single is None:
        return None, failure_response(name + " not found")
    return single, None

def missing_args_check(keys, body):
    values = []
    for key in keys:
        v = body.get(key)
        if v is None:
            return None, failure_response("missing arguments", 400)
        values.append(v)
    return tuple(values), None


    
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
    v, err = missing_args_check(("code", "name"), body)
    if err is not None:
        return err
    code, name = v
    new_course = Course(code=code, name=name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course_by_id(course_id):
    """
    Endpoint for getting a course by id
    """
    course, err = single_not_found_check(course_id, Course, "course")
    if err is not None:
        return err
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for delteing a course by id
    """
    course, err = single_not_found_check(course_id, Course, "course")
    if err is not None:
        return err
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    v, err = missing_args_check(("name", "netid"), body)
    if err is not None:
        return err
    name, netid = v
    new_user = User(name=name, netid=netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user_by_id(user_id):
    """
    Endpoint fo getting a user by id
    """
    user, err = single_not_found_check(user_id, User, "user")
    if err is not None: return err
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a user to a course by id
    """
    course, err = single_not_found_check(course_id, Course, "course")
    if err is not None: return err
    body = json.loads(request.data)
    v, err = missing_args_check(("user_id",), body)
    if err is not None: return err
    user_id = v[0]
    user, err = single_not_found_check(user_id, User, "user")
    if err is not None: return err

    type = body.get("type")
    if type not in ["student", "instructor"]:
        return failure_response("type must be student or instructor", 400)
    if type == "student": course.students.append(user)
    if type == "instructor": course.instructors.append(user)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    endpoint for creating an assignment for a course by id
    """
    _, err = single_not_found_check(course_id, Course, "course")
    if err is not None:
        return err
    body = json.loads(request.data)
    v, err = missing_args_check(("title", "due_date"), body)
    if err is not None:
        return err
    title, due_date = v
    new_assignment = Assignment(
        title=title,
        due_date=due_date,
        course_id=course_id,
    )
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
