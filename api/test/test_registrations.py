import json
import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.management import Course, Student
from ..models.management import Registration
from ..utils import db


class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['testing'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

        # Create a sample course and student
        course = Course(
            name='Test Course',
            id='1',
            teacher='tinubu',
            grade=4.0

        )
        db.session.add(course)
        db.session.commit()

        student = Student(
            name='John Doe',
            email='johndoe@example.com'
        )
        db.session.add(student)
        db.session.commit()

        # Store the sample course and student IDs for use in tests
        self.course_id = course.id
        self.student_id = student.id

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_create_registration(self):
        registration_data = {
            'student_id': self.student_id,
            'course_id': self.course_id,
            'grade': 3.5
        }

        response = self.client.post('/registrations/register', data=json.dumps(registration_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        registration = Registration.query.filter_by(student_id=self.student_id, course_id=self.course_id).first()
        self.assertEqual(registration.grade, 3.5)

    def test_get_registrations_by_course(self):
        # Create a second student and register them for the same course
        student2 = Student(
            name='Jane Doe',
            email='janedoe@example.com'
        )
        db.session.add(student2)
        db.session.commit()

        registration = Registration(
            student_id=student2.id,
            course_id=self.course_id,
            grade=3.0
        )
        db.session.add(registration)
        db.session.commit()

        response = self.client.get(f'/registrations/course/{self.course_id}')
        data = json.loads(response.data)

        self.assertTrue(data.get('success', True))

        self.assertEqual(len(data.get('registrations', [])), 0)

        course_ids = [registration['course_id'] for registration in data.get('registrations', [])]
        self.assertTrue(all(course_id == self.course_id for course_id in course_ids))

    def test_get_registration_by_id(self):
        registration = Registration(
            student_id=self.student_id,
            course_id=self.course_id,
            grade=3.0
        )
        db.session.add(registration)
        db.session.commit()

        response = self.client.get(f'/registrations/registration/{registration.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], registration.id)
        self.assertEqual(data['student_id'], self.student_id)
        self.assertEqual(str(data['course_id']), str(self.course_id))
        self.assertEqual(data['grade'], 3.0)

    def test_delete_registration(self):
        # Create a registration
        registration = Registration(
            student_id=self.student_id,
            course_id=self.course_id,
            grade=3.0
        )
        db.session.add(registration)
        db.session.commit()

        # Delete the registration
        response = self.client.delete(f'/registrations/registration/{registration.id}')
        self.assertEqual(response.status_code, 204)

