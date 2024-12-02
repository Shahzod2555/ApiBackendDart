from marshmallow import fields, ValidationError, validates_schema, validates, Schema
import re

class UserSchema(Schema):
    email = fields.Email(allow_none=True)
    phone_number = fields.String(allow_none=True)
    password = fields.String(required=True, validate=lambda x: len(x) >= 6)

    @validates_schema
    def validate_at_least_one(self, data, **kwargs):
        if not any([data.get('email'), data.get('phone_number')]):
            raise ValidationError("Введите корректные данные")

    @validates('phone_number')
    def validate_phone_number(self, value):
        if value and not re.match(r'^(?:\+7\d{10}|8\d{10})$', value):
            raise ValidationError("Некорректный номер телефона. Ожидается формат +7XXXXXXXXXX или 8XXXXXXXXXX.")
