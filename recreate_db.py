from random import randint
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Job, Category, Department, engine


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

categories = [Category(name='Deployment'),
              Category(name='Construction'),
              Category(name='Research'),
              Category(name='Exploration')]

for category in categories:
    session.add(category)
session.commit()

print('\nCategories have been successfully added to the database')

departments = [Department(title='Geological Survey', chief=1,
                          members='2,3', email='geo_surv@mars.org'),
               Department(title='Engineering', chief=10,
                          members='12,13,14', email='eng@mars.org')]

for department in departments:
    session.add(department)
session.commit()

print('\nDepartments have been successfully added to the database')

colonists_data = [
    {
        'surname': 'Scott',
        'name': 'Ridley',
        'age': 21,
        'position': 'captain',
        'speciality': 'research engineer',
        'address': 'module_1',
        'email': 'scott_chief@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Smith',
        'name': 'John',
        'age': 30,
        'position': 'engineer',
        'speciality': 'mechanical engineer',
        'address': 'module_2',
        'email': 'smith_john@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Johnson',
        'name': 'Emily',
        'age': 25,
        'position': 'biologist',
        'speciality': 'microbiologist',
        'address': 'module_3',
        'email': 'johnson_emily@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Williams',
        'name': 'James',
        'age': 28,
        'position': 'geologist',
        'speciality': 'rock specialist',
        'address': 'module_4',
        'email': 'williams_james@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Brown',
        'name': 'Sarah',
        'age': 29,
        'position': 'chemist',
        'speciality': 'organic chemist',
        'address': 'module_5',
        'email': 'brown_sarah@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Jones',
        'name': 'Michael',
        'age': 27,
        'position': 'physicist',
        'speciality': 'quantum physicist',
        'address': 'module_6',
        'email': 'jones_michael@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Alexander',
        'name': 'Brown',
        'age': 20,
        'position': 'chef',
        'speciality': 'italian chef',
        'address': 'module_1',
        'email': 'alex.brown@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Joshua',
        'name': 'Graham',
        'age': 14,
        'position': 'child',
        'speciality': None,
        'address': 'module_4',
        'email': 'cool.josh@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Jasmine',
        'name': 'Briggs',
        'age': 11,
        'position': 'child',
        'speciality': None,
        'address': 'module_3',
        'email': 'jbriggs@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Taylor',
        'name': 'Rachel',
        'age': 35,
        'position': 'chief engineer',
        'speciality': 'mechanical engineer',
        'address': 'module_1',
        'email': 'taylor_rachel@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Evans',
        'name': 'Oliver',
        'age': 40,
        'position': 'middle biologist',
        'speciality': 'microbiologist',
        'address': 'module_2',
        'email': 'evans_oliver@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Roberts',
        'name': 'Emma',
        'age': 38,
        'position': 'chief geologist',
        'speciality': 'rock specialist',
        'address': 'module_3',
        'email': 'roberts_emma@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'King',
        'name': 'Ethan',
        'age': 32,
        'position': 'middle chemist',
        'speciality': 'organic chemist',
        'address': 'module_4',
        'email': 'king_ethan@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Morgan',
        'name': 'Ava',
        'age': 37,
        'position': 'chief physicist',
        'speciality': 'quantum physicist',
        'address': 'module_5',
        'email': 'morgan_ava@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Sophia',
        'name': 'Clark',
        'age': 10,
        'position': 'child',
        'speciality': None,
        'address': 'module_1',
        'email': 'sophia_clark@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    },
    {
        'surname': 'Liam',
        'name': 'Dawson',
        'age': 9,
        'position': 'child',
        'speciality': None,
        'address': 'module_1',
        'email': 'liam_dawson@mars.org',
        'hashed_password': 'some_hashed_password',
        'modified_date': datetime.now()
    }
]

for colonist_data in colonists_data:
    colonist = User(**colonist_data)
    session.add(colonist)

session.commit()

print('\nUsers have been successfully added to the database')

jobs_data = [
    {
        'team_leader': 1,
        'job': 'deployment of residential modules 1 and 2',
        'work_size': 15,
        'collaborators': '2, 3',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 1,
        'job': 'maintenance of life support systems',
        'work_size': 10,
        'collaborators': '4, 5',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 2,
        'job': 'environmental research',
        'work_size': 18,
        'collaborators': '1, 3',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 3,
        'job': 'mineral exploration',
        'work_size': 22,
        'collaborators': '2, 4',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 4,
        'job': 'chemical analysis of soil samples',
        'work_size': 8,
        'collaborators': '1, 5',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 5,
        'job': 'maintenance of power supply systems',
        'work_size': 12,
        'collaborators': '2, 3',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 6,
        'job': 'meteorological observations',
        'work_size': 16,
        'collaborators': '1, 4',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 7,
        'job': 'construction of new modules',
        'work_size': 25,
        'collaborators': '3, 5',
        'start_date': datetime.now(),
        'is_finished': False
    },
    {
        'team_leader': 12,
        'job': 'digging a quarry',
        'work_size': 30,
        'collaborators': '13, 14',
        'start_date': datetime.now(),
        'is_finished': False
    }
]

for job_data in jobs_data:
    job = Job(**job_data)

    job.categories.append(categories[randint(0, 3)])

    session.add(job)

session.commit()

print('\nJobs have been successfully added to the database')
