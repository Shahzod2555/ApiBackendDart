from flask import Blueprint, request, jsonify
from ..forms.form_login import UserSchema
from marshmallow import ValidationError
from ..extends import db, bcrypt
from ..models.user import User

register = Blueprint('register_blueprint', __name__)

@register.route('/register', methods=['POST'])
def register_endpoint():
    user_schema = UserSchema()
    try:
        print("Полученные данные:", request.json)
        data = user_schema.load(request.json)
        print("Валидированные данные:", data)

        if data['email']:
            existing_user = User.query.filter_by(email=data['email']).first()
            print("Существующий пользователь (email):", existing_user)
            if existing_user:
                return jsonify({"error": "Пользователь с таким email уже существует."}), 400

            hash_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user_new = User(email=data['email'], phone_number=data['phone_number'], password=hash_password)
            db.session.add(user_new)
            db.session.commit()
            print("Пользователь успешно зарегистрирован:", user_new)
            return jsonify({'user': data['email'] or data['phone_number'], 'message': 'Пользователь успешно зарегистрирован.'}), 200
        
    except ValidationError as err:
        print("Ошибка валидации:", err.messages)
        return jsonify({"error": err.messages}), 400

    except Exception as error:
        print(f"Внутренняя ошибка: {error}")
        return jsonify({"error": "Внутренняя ошибка сервера. Попробуйте позже."}), 500
