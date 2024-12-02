from marshmallow import ValidationError
from ..forms.form_login import UserSchema
from flask import Blueprint, request, jsonify
from ..models.user import User
from flask_login import login_user
import logging

login = Blueprint('login_blueprint', __name__)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@login.route('/login', methods=['POST'])
def login_endpoint():
    user_schema = UserSchema()
    try:
        logger.info(f"Полученные данные: {request.json}")
        data = user_schema.load(request.json)
        logger.info(f"Валидированные данные: {data}")

        if not data.get('email') and not data.get('phone_number'):
            logger.error("Необходимо указать хотя бы email или номер телефона.")
            return jsonify({"error": "Необходимо указать хотя бы email или номер телефона."}), 400

        user = None
        identifier = None
        if data.get('email'):
            user = User.query.filter_by(email=data['email']).first()
            identifier = "email"
        elif data.get('phone_number'):
            user = User.query.filter_by(phone_number=data['phone_number']).first()
            identifier = "номером телефона"
        if user:
            logger.info(f"Существующий пользователь ({identifier}): {user}")
            login_user(user)
            user_data = {
                "id": user.id,
                "email": user.email,
                "phone_number": user.phone_number,
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else None
            }
            return jsonify({"message": "Пользователь успешно авторизован.", "user": user_data}), 200
        else:
            logger.error(f"Пользователь с указанным {identifier} не найден.")
            return jsonify({"error": f"Пользователь с указанным {identifier} не найден."}), 400

    except ValidationError as err:
        logger.error(f"Ошибка валидации: {err.messages}")
        return jsonify({"error": err.messages}), 400

    except Exception as error:
        logger.error(f"Внутренняя ошибка: {error}")
        return jsonify({"error": "Внутренняя ошибка сервера. Попробуйте позже."}), 500
