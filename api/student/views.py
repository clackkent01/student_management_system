from flask_restx import Namespace, Resource, fields
from ..utils import db
from ..models.management import Student

student_namespace = Namespace('Student', description="a namespace for student ")

student_model = student_namespace.model('Student', {
    'id': fields.Integer(readOnly=True, description='The student unique identifier'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email address'),
    'courses': fields.List(fields.Integer, description='The IDs of the courses the student is enrolled in')
})


@student_namespace.route('/student')
class StudentList(Resource):

    # Create a student
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model, code=201)
    def post(self):
        """
            create a  student
        :return:
        """
        student = Student(
            id=student_namespace.payload['id'],
            name=student_namespace.payload['name'],
            email=student_namespace.payload['email']
        )
        db.session.add(student)
        db.session.commit()
        return student

    # Get all students
    @student_namespace.marshal_list_with(student_model)
    def get(self):
        """
            get all created students
        :return:
        """
        students = Student.query.all()
        return students


@student_namespace.route('/student/<int:id>')
class StudentDetails(Resource):

    # Update a student
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    def put(self, id):
        """
            update a student
        :param id:
        :return:
        """
        student = Student.query.filter_by(id=id).first()
        if student:
            student.id = student_namespace.payload['id']
            student.name = student_namespace.payload['name']
            student.email = student_namespace.payload['email']
            db.session.commit()
        return student

    # Delete a student
    @student_namespace.response(204, 'Student deleted successfully')
    def delete(self, id):
        """
            delete a student
        :param id:
        :return:
        """
        student = Student.query.filter_by(id=id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
        return None, 204

    # Get a student by ID
    @student_namespace.marshal_with(student_model)
    def get(self, id):
        student = Student.query.filter_by(id=id).first()
        return student
