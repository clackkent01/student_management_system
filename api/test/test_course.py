import json
import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.management import Student, Course, Grade
from ..utils import db
from http import HTTPStatus


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['testing'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_calculate_total_grade(self):
        # Create a student
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        response = self.client.post('/student/student', data=json.dumps(student_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Create some grades for the student
        grades_data = [
            {
                'student_id': 1,
                'course_id': 'CSC101',
                'score': 80,
                'credit': 3
            },
            {
                'student_id': 1,
                'course_id': 'PHY101',
                'score': 75,
                'credit': 4
            },
            {
                'student_id': 1,
                'course_id': 'MAT101',
                'score': 90,
                'credit': 3
            }
        ]

        for grade_data in grades_data:
            response = self.client.post('/course/grade', data=json.dumps(grade_data),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)

        # Get the total grade for the student
        response = self.client.get('/course/course/1/total_grade')
        self.assertEqual(response.status_code, 400)

        total_grade = response.json
        self.assertEqual(total_grade, 3.44)

    def test_course_list(self):
        # Create some courses to test the endpoint
        course1 = Course(id='COMP101', name='Introduction to Computer Science', teacher='John Smith', grade=0.0)
        course2 = Course(id='MATH101', name='Calculus I', teacher='Mary Johnson', grade=0.0)
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()

        # Send a GET request to the endpoint and check the response
        response = self.client.get('/course/course')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json), 2)

    def test_create_course(self):
        # Send a POST request to create a new course
        data = {
            'id': 'ENGL101',
            'name': 'Introduction to Literature',
            'teacher': 'Jane Doe'
        }
        response = self.client.post('/course/course', json=data)

        # Check that the course was created
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json['id'], 'ENGL101')
        self.assertEqual(response.json['name'], 'Introduction to Literature')
        self.assertEqual(response.json['teacher'], 'Jane Doe')

        # Check that the course exists in the database
        course = Course.query.filter_by(id='ENGL101').first()
        self.assertIsNotNone(course)

    def test_update_course(self):
        # Create a course to update
        course = Course(id='CHEM101', name='General Chemistry', teacher='Bob Johnson', grade=0.0)
        db.session.add(course)
        db.session.commit()

        # Send a PUT request to update the course
        data = {
            'id': 'CHEM101',
            'name': 'Chemistry for Beginners',
            'teacher': 'Alice Brown'
        }
        response = self.client.put('/course/course', json=data)

        # Check that the course was updated
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json['id'], 'CHEM101')
        self.assertEqual(response.json['name'], 'Chemistry for Beginners')
        self.assertEqual(response.json['teacher'], 'Alice Brown')

        # Check that the course was updated in the database
        updated_course = Course.query.filter_by(id='CHEM101').first()
        self.assertIsNotNone(updated_course)
        self.assertEqual(updated_course.name, 'Chemistry for Beginners')
        self.assertEqual(updated_course.teacher, 'Alice Brown')
