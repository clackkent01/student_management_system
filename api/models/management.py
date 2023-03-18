from ..utils import db


class Course(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Float, nullable=False, default=0.0)
    teacher = db.Column(db.String(50), nullable=False)
    registrations = db.relationship('Registration', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.id}: {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    registrations = db.relationship('Registration', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    score = db.Column(db.Float, nullable=False)
    credit = db.Column(db.Integer, default=0)

    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
    course = db.relationship('Course', backref=db.backref('grades', lazy=True))

    def __repr__(self):
        return f'<Registration {self.id}: Student {self.student_id} - Course {self.course_id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


# Define the Registration model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=True, default=0.0)

    def __repr__(self):
        return f'<Registration {self.id}: Student {self.student_id} - Course {self.course_id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
