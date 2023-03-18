from flask import request
from flask_restx import Namespace, fields, Resource
from ..utils import db
from ..models.management import Course, Student, Grade

course_namespace = Namespace('Course', description="Namespace for course")

course_model = course_namespace.model('Course', {
    'id': fields.String(readOnly=True, description='The course unique identifier'),
    'name': fields.String(required=True, description='The course name'),
    'teacher': fields.String(required=True, description='The teacher name')
})
grade_model = course_namespace.model('Grade', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a grade'),
    'student_id': fields.Integer(required=True, description='The unique identifier of the student'),
    'course_id': fields.String(required=True, description='The unique identifier of the course'),
    'credit': fields.Integer(required=True, description='The credit of the course'),
    'score': fields.Float(required=True, description='The score earned by the student in the course')
})


@course_namespace.route('/course')
class CourseList(Resource):
    @course_namespace.marshal_list_with(course_model)
    @course_namespace.doc(
        description="get  Course ",
    )
    def get(self):
        """
            get course
        :return:
        """
        courses = Course.query.all()
        return courses

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model, code=201)
    @course_namespace.doc(
        description="Crate a New Course ",
    )
    def post(self):
        """
            create course
        :return:
        """
        course = Course(
            name=course_namespace.payload['name'],
            teacher=course_namespace.payload['teacher'],
            id=course_namespace.payload['id']
        )
        db.session.add(course)
        db.session.commit()
        return course, 201

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description="update a  Course ",
    )
    def put(self):
        """
            update course
        :return:
        """
        course = Course.query.filter_by(id=course_namespace.payload['id']).first()
        if course:
            course.name = course_namespace.payload['name']
            course.teacher = course_namespace.payload['teacher']
            course.id = course_namespace.payload['id']
            db.session.commit()
        return course

    @course_namespace.expect(course_model)
    @course_namespace.doc(
        description="delete a New Course ",
    )
    def delete(self):
        """
            delete course
        :return:
        """
        course = Course.query.filter_by(id=course_namespace.payload['id']).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return {'message': f'Course with id {course.id} has been deleted'}
        else:
            return {'error': 'Course not found'}


@course_namespace.expect(course_model)
@course_namespace.marshal_with(course_model)
def put(self):
    course = Course.query.filter_by(id=course_namespace.payload['id']).first()
    if course:
        course.name = course_namespace.payload['name']
        course.teacher = course_namespace.payload['teacher']
        course.grade = course_namespace.payload['grade']
        db.session.commit()
    return course


@course_namespace.route('/<int:student_id>/grade/<int:course_id>')
class Grade(Resource):
    @course_namespace.expect(grade_model)
    @course_namespace.response(201, 'Grade successfully created.')
    @course_namespace.doc(
        description="grade a Course ",
    )
    def post(self, student_id, course_id):
        """
            grade a course
        :param student_id:
        :param course_id:
        :return:
        """
        # Get the student and course objects
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)

        # Check if the student and course exist
        if not student or not course:
            return {'message': 'Invalid student or course ID'}, 404

        # Get the grade data from the request
        grade_data = request.json

        # Check if the credit and score fields are present in the request data
        if 'credit' not in grade_data or 'score' not in grade_data:
            return {'message': 'Credit and score fields are required.'}, 400

        # Check if the credit and score fields are valid
        credit = grade_data['credit']
        score = grade_data['score']
        if not isinstance(credit, int) or not isinstance(score, float):
            return {'message': 'Invalid credit or score.'}, 400

        # Create a new grade object and save it to the database
        grade = Grade(student=student, course=course, credit=credit, score=score)
        db.session.add(grade)
        db.session.commit()

        # Return a response indicating that the grade was successfully created
        return {'message': 'Grade successfully created.'}, 201


@course_namespace.route('/course/<int:student_id>/total_grade')
@course_namespace.doc(
        description="total grades for Course ",
    )
class TotalGrade(Resource):
    """
        calculate total grade
    """
    def get(self, student_id):
        # Get all grades for the given student
        student_grades = Grade.query.filter_by(student_id=student_id).all()

        # Initialize variables for total grade points and total credits
        total_grade_points = 0
        total_credits = 0

        # Iterate over all grades for the student
        for grade in student_grades:
            # Get the credits and score for the current grade
            credits = grade.credit
            score = grade.score

            # Convert the score to the 4.0 grading scale
            if score >= 90:
                grade_points = 4.0
            elif score >= 80:
                grade_points = 3.0
            elif score >= 70:
                grade_points = 2.0
            elif score >= 60:
                grade_points = 1.0
            else:
                grade_points = 0.0

            total_grade_points += grade_points * credits

            total_credits += credits

        if total_credits == 0:
            total_grade = 0.0
        else:
            total_grade = total_grade_points / total_credits

        # Return the total grade
        return round(total_grade, 2)
