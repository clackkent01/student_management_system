from flask import Flask
from flask_restx import Api
from .student.views import student_namespace
from .course.views import course_namespace
from .auth.views import auth_namespace
from .registrations.views import registration_namespace
from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from .models.users import User
from .models.management import Student, Registration, Course


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)
    authorizations = {
        "Bearer Auth": {
            'type': "apikey",
            'in': 'header',
            'name': "Authorization",
            'description': "Add a jwt with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    api = Api(app,
              title="student-Management-system",
              description="A REST API for Student Management",
              authorizations=authorizations,
              security="Bearer Auth"
              )

    api.add_namespace(student_namespace, path='/student')
    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(registration_namespace, path='/registrations')
    api.add_namespace(auth_namespace, path='/')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course,
            'Student': Student,
            'Registration': Registration

        }

    return app
