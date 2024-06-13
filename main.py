from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.orm import sessionmaker, joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Image, Vote, engine
from generate_image import generate_and_save_images
import os

app = Flask(__name__)
app.secret_key = 'top_secret_key'

DataBase_Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    db_session = DataBase_Session()
    images = db_session.query(Image).options(
        joinedload(Image.author_user)).all()
    db_session.close()

    if 'user_id' in session:
        user_id = session['user_id']
        db_session = DataBase_Session()
        user = db_session.query(User).filter_by(id=user_id).first()
        db_session.close()
        return render_template('main_page.html', user=user, images=images)
    else:
        return render_template('main_page.html', user=None, images=images)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Пароли не совпадают"

        hashed_password = generate_password_hash(password)
        new_user = User(
            surname=surname,
            name=name,
            age=age,
            email=email,
            hashed_password=hashed_password,
            modified_date=datetime.now()
        )

        db_session = DataBase_Session()
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

        return redirect(url_for('registration_success'))
    return render_template('register.html')


@app.route('/registration_success')
def registration_success():
    return "Вы успешно зарегистрировались!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db_session = DataBase_Session()
        user = db_session.query(User).filter_by(email=email).first()

        if user and (check_password_hash(user.hashed_password, password) or (user.id == 1 and user.hashed_password == password)):
            session['user_id'] = user.id
            db_session.close()
            return redirect(url_for('index'))
        db_session.close()
        return "Неверный email или пароль"

    return render_template('login.html')


@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    image_path = generate_and_save_images()
    session['generated_image_path'] = image_path

    return redirect(url_for('add_image'))


@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    generated_image_path = session.get('generated_image_path')
    if not generated_image_path:
        generated_image_path = generate_and_save_images()

    if request.method == 'POST':
        title = request.form['title']
        prompt = request.form['prompt']
        author = session['user_id']
        generation_date = datetime.now()

        new_image = Image(
            title=title,
            author=author,
            prompt=prompt,
            generation_date=generation_date,
            file_path=generated_image_path
        )

        db_session = DataBase_Session()
        db_session.add(new_image)
        db_session.commit()
        db_session.close()

        session.pop('generated_image_path', None)
        return redirect(url_for('index'))

    return render_template('add_image.html', generated_image_path=generated_image_path)


@app.route('/edit_image/<int:image_id>', methods=['GET', 'POST'])
def edit_image(image_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_session = DataBase_Session()
    image = db_session.query(Image).filter_by(id=image_id).first()

    if not image:
        db_session.close()
        return "Изображение не найдено", 404

    # Проверяем, является ли пользователь автором поста или админом (user_id == 1)
    if session['user_id'] != image.author and session['user_id'] != 1:
        db_session.close()
        return "Вы не имеете права редактировать это изображение", 403

    if request.method == 'POST':
        title = request.form['title']
        prompt = request.form['prompt']

        image.title = title
        image.prompt = prompt
        image.modified_date = datetime.now()

        db_session.commit()
        db_session.close()

        return redirect(url_for('index'))

    db_session.close()
    return render_template('edit_image.html', image=image)


@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db_session = DataBase_Session()
    image = db_session.query(Image).filter_by(id=image_id).first()

    if image and image.author == session['user_id']:
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        db_session.delete(image)
        db_session.commit()
    db_session.close()
    return redirect(url_for('index'))


@app.route('/upvote/<int:image_id>', methods=['POST'])
def upvote(image_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db_session = DataBase_Session()

    existing_vote = db_session.query(Vote).filter_by(
        user_id=user_id, image_id=image_id).first()
    if existing_vote:
        if existing_vote.vote_type == 'upvote':
            return redirect(url_for('index'))
        else:
            existing_vote.vote_type = 'upvote'
            image = db_session.query(Image).filter_by(id=image_id).first()
            image.rating += 2
            db_session.commit()
            db_session.close()
            return redirect(url_for('index'))

    new_vote = Vote(user_id=user_id, image_id=image_id, vote_type='upvote')
    image = db_session.query(Image).filter_by(id=image_id).first()
    if image:
        image.rating += 1
        db_session.add(new_vote)
        db_session.commit()
    db_session.close()
    return redirect(url_for('index'))


@app.route('/downvote/<int:image_id>', methods=['POST'])
def downvote(image_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db_session = DataBase_Session()

    existing_vote = db_session.query(Vote).filter_by(
        user_id=user_id, image_id=image_id).first()
    if existing_vote:
        if existing_vote.vote_type == 'downvote':
            return redirect(url_for('index'))
        else:
            existing_vote.vote_type = 'downvote'
            image = db_session.query(Image).filter_by(id=image_id).first()
            image.rating -= 2
            db_session.commit()
            db_session.close()
            return redirect(url_for('index'))

    new_vote = Vote(user_id=user_id, image_id=image_id, vote_type='downvote')
    image = db_session.query(Image).filter_by(id=image_id).first()
    if image:
        image.rating -= 1
        db_session.add(new_vote)
        db_session.commit()
    db_session.close()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
