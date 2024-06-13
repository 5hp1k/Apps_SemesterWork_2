from datetime import datetime
from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Image, engine
from generate_image import generate_and_save_images
from flask import Blueprint


api = Blueprint('api', __name__)

DataBase_Session = sessionmaker(bind=engine)


@api.route('/images', methods=['GET'])
def get_images():
    db_session = DataBase_Session()
    images = db_session.query(Image).all()
    db_session.close()
    return jsonify([image.to_dict() for image in images])


@api.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    db_session = DataBase_Session()
    image = db_session.query(Image).filter_by(id=image_id).first()
    db_session.close()
    if image:
        return jsonify(image.to_dict())
    return jsonify({'error': 'Изображение не найдено'}), 404


@api.route('/images', methods=['POST'])
def create_image():
    if 'user_id' not in session:
        return jsonify({'error': 'Неавторизованный доступ'}), 401

    generated_image_path = generate_and_save_images()

    title = request.json.get('title')
    prompt = request.json.get('prompt')
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

    return jsonify(new_image.to_dict()), 201


@api.route('/images/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Неавторизованный доступ'}), 401

    db_session = DataBase_Session()
    image = db_session.query(Image).filter_by(id=image_id).first()

    if not image:
        db_session.close()
        return jsonify({'error': 'Изображение не найдено'}), 404

    if session['user_id'] != image.author and session['user_id'] != 1:
        db_session.close()
        return jsonify({'error': 'Нет прав для редактирования изображения'}), 403

    title = request.json.get('title')
    prompt = request.json.get('prompt')

    image.title = title
    image.prompt = prompt
    image.modified_date = datetime.now()

    db_session.commit()
    db_session.close()

    return jsonify(image.to_dict())


@api.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Неавторизованный доступ'}), 401

    db_session = DataBase_Session()
    image = db_session.query(Image).filter_by(id=image_id).first()

    if not image:
        db_session.close()
        return jsonify({'error': 'Изображение не найдено'}), 404

    if image.author != session['user_id'] and session['user_id'] != 1:
        db_session.close()
        return jsonify({'error': 'Нет прав для удаления изображения'}), 403

    if os.path.exists(image.file_path):
        os.remove(image.file_path)
    db_session.delete(image)
    db_session.commit()
    db_session.close()

    return jsonify({'message': 'Изображение удалено'})
