from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#assoc tables
students_association_table = db.Table(
    "students_course_user_association",
    db.Model.metadata,
    db.Column("course_id",db.Integer,db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

instructors_association_table = db.Table(
    "instructor_course_user_association",
    db.Model.metadata,
    db.Column("course_id",db.Integer,db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)


# your classes here
class Course(db.Model):
    """
    Course model
    one-to-many relationship with Assignment model
    many-to-many relationship with User model
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User",secondary=instructors_association_table, back_populates="courses_instructor")
    students = db.relationship("User", secondary=students_association_table, back_populates="courses_student")

    def __init__(self, **kwargs):
        """
        Initialize Course object/entry
        """
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serialize a Course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name":self.name,
            "assignments": [a.simple_serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students": [s.simple_serialize() for s in self.students],
        }
    
    def simple_serialize(self):
        """
        Serialize a Course object without its relationships
        """
        return {
            "id": self.id,
            "code": self.code,
            "name":self.name,
        }
    

class Assignment(db.Model):
    """
    Assignment model
    one-to-many relationship with Course model
    """
    __tablename__ = "assignment"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    course = db.relationship("Course", back_populates="assignments")
    
    def __init__(self, **kwargs):
        """
        Initializes an Assignment object
        """
        self.title = kwargs.get("title")
        self.due_date = kwargs.get("due_date")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        """
        serialize an assignment object
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": self.course.simple_serialize(),
        }
    
    def simple_serialize(self):
        """
        serialize an assignment object without relationships
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
        }


class User(db.Model):
    """
    User model
    many-to-many relationship with Course model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses_instructor = db.relationship("Course", secondary=instructors_association_table, back_populates="instructors")
    courses_student = db.relationship("Course", secondary=students_association_table, back_populates="students")

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name = kwargs.get("name")
        self.netid = kwargs.get("netid")

    def all_courses(self):
        course_ids = {}
        for course in self.courses_student + self.courses_instructor:
            course_ids[course.id] = course
        return [c.simple_serialize() for c in course_ids.values()]

    def serialize(self):
        """
        serialize a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": self.all_courses(),
        }
    
    def simple_serialize(self):
        """
        serialize a user object EXCEPT the course
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
        }