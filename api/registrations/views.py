from flask_restx import Namespace, Resource, fields
from ..models.management import Registration
from ..utils import db

registration_namespace = Namespace('registration', description="Name space for registrations")

registration_model = registration_namespace.model('Registration', {
    'id': fields.Integer(readOnly=True, description='The  unique identifier'),
    'student_id': fields.Integer(required=True, description='The student identifier'),
    'course_id': fields.Integer(required=True, description='The course identifier'),
    'grade': fields.Float(description='The grade received by the student in the course')
})


@registration_namespace.route('/register')
class RegistrationList(Resource):
    @registration_namespace.expect(registration_model)
    @registration_namespace.marshal_with(registration_model, code=201)
    def post(self):
        """
            register for a course
        :return:
        """
        registration = Registration(
            student_id=registration_namespace.payload['student_id'],
            course_id=registration_namespace.payload['course_id'],
            grade=registration_namespace.payload['grade']
        )
        db.session.add(registration)
        db.session.commit()
        return registration


@registration_namespace.route('/course/<int:course_id>')
class RegistrationByCourse(Resource):
    @registration_namespace.marshal_list_with(registration_model)
    def get(self, course_id):
        """
            retrieve all courses
        :param course_id:
        :return:
        """
        registrations = Registration.query.filter_by(course_id=course_id).all()
        return registrations


@registration_namespace.route('registration/<int:id>')
class Registration(Resource):
    @registration_namespace.marshal_with(registration_model)
    def get(self, id):
        """
            get all registrations
        :param id:
        :return:
        """
        registration = Registration.query.get(id)
        if registration:
            return registration, 200
        else:
            return {'message': 'Registration not found'}, 404

    def delete(self, id):
        """
            delete registration
        :param id:
        :return:
        """
        registration = Registration.query.get(id)
        if registration:
            db.session.delete(registration)
            db.session.commit()
            return {'message': 'Registration deleted'}, 204
        else:
            return {'message': 'Registration not found'}, 404
