from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Image, Vote, engine


# Удаление всех таблиц и создание заново
Base.metadata.drop_all(engine)
print('\nDatabase has been dropped')

Base.metadata.create_all(engine)
print('\nDatabase has been created')

Session = sessionmaker(bind=engine)
session = Session()

# Добавление пользователей
user_data = [
    User(surname='Admin', name='Admin', age=512, email='admin@ml.com',
         hashed_password='123', modified_date=datetime.now())
]

for user in user_data:
    session.add(user)
session.commit()
print('\nUsers have been successfully added to the database')

# Добавление изображений
image_data = [
    Image(title='First Image', author=1, prompt='Первая картинка',
          generation_date=datetime.now(), rating=5)
]

for image in image_data:
    session.add(image)
session.commit()
print('\nImages have been successfully added to the database')

# Добавление голосов
vote_data = [
    Vote(user_id=1, image_id=1, vote_type='upvote')
]

for vote in vote_data:
    session.add(vote)
session.commit()

print('\nVotes have been successfully added to the database')
print('\nDatabase has successfully been reset')
