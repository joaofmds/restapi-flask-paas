from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel, HealthCheckModel
import re


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "first_name", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "last_name", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "cpf", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "email", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "birth_date", type=str, required=True, help="This field cannot be blank."
)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def validateCpf(self, cpf):
        if not re.match(r"\d{3}\.\d{3}\.\d{3}\-\d{2}", cpf):
            return False

        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validateCpf(data.cpf):
            return {"message": "CPF is invalid."}, 400
        try:
            response = UserModel(**data).save()
            return {"message": f"User {response.id} successfully created!"}
        except NotUniqueError:
            return {"message": "CPF already exists in database!"}, 400

    def patch(self):
        data = _user_parser.parse_args()

        if not self.validateCpf(data.cpf):
            return {"message": "CPF is invalid."}, 400

        response = UserModel.objects(cpf=data.cpf).first()
        if response:
            response.update(**data)
            return {"message": "User updated!"}, 200
        else:
            return {"message": "User does not exist in database!"}, 400


class UserDetail(Resource):
    def get(self, cpf):
        user = UserModel.objects(cpf=cpf).first()

        if user:
            return jsonify(user)
        else:
            return {"message": "User does not exist in data"}, 404

    def delete(self, cpf):
        try:
            response = UserModel.objects(cpf=cpf).first()

            if response:
                response.delete()
                return {"message": "User deleted!"}, 200
            else:
                return {"message": "User does not exist in database!"}, 404
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500


class HealthCheck(Resource):
    def get(self):
        response = HealthCheckModel.objects(status="healthcheck")
        if response:
            return "Healthy", 200
        else:
            HealthCheckModel(status="healthcheck").save()
            return "Healthy", 200
