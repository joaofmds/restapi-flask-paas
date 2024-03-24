import pytest
from application import create_app


class TestApplication:
    @pytest.fixture
    def client(self):
        app = create_app("config.MockConfig")
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Felipe",
            "last_name": "Mendes",
            "cpf": "501.933.250-04",
            "email": "felipe@gmail.com",
            "birth_date": "1999-04-06",
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Felipe",
            "last_name": "Mendes",
            "cpf": "501.933.250-05",
            "email": "felipe@gmail.com",
            "birth_date": "1999-04-06",
        }

    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post("/user", json=valid_user)
        assert response.status_code == 200
        assert b"successfully" in response.data

        response = client.post("/user", json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get(f'/user/{valid_user["cpf"]}')
        assert response.status_code == 200
        data = response.json
        assert data["first_name"] == "Felipe"
        assert data["last_name"] == "Mendes"
        assert data["cpf"] == "501.933.250-04"
        assert data["email"] == "felipe@gmail.com"
        assert data["birth_date"]["$date"] == "1999-04-06T00:00:00Z"

        response = client.get(f'/user/{invalid_user["cpf"]}')
        assert response.status_code == 404
        assert b"User does not exist in data" in response.data

    def test_patch_user(self, client, valid_user):
        valid_user["first_name"] = "João"
        response = client.patch("/user", json=valid_user)
        assert response.status_code == 200
        assert b"User updated!" in response.data

        valid_user["cpf"] = "940.494.970-18"
        response = client.patch("/user", json=valid_user)
        assert response.status_code == 400
        assert b"does not exist in database" in response.data

    def test_delete_user(self, client, valid_user):
        response = client.delete(f'/user/{valid_user["cpf"]}')
        assert response.status_code == 200
        assert b"deleted" in response.data

        response = client.delete(f'/user/{valid_user["cpf"]}')
        assert response.status_code == 404
        assert b"does not exist" in response.data
