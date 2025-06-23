from http import HTTPStatus

from project.schemas import UserPublic


def test_hello_world(client):
    # client = TestClient(app)  # Arrange substituido por fixture

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_html(client):

    response = client.get("/hello")

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.text == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            'username': 'Victor',
            'email': 'victor@teste.com',
            'password': 'tangerina123',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Victor',
        'email': 'victor@teste.com',
        'id': 1,
    }

    response_error_name = client.post(
        "/users/",
        json={
            'username': 'Victor',
            'email': 'victormanjericao@teste.com',
            'password': 'entrandonaconta2918',
        }
    )

    assert response_error_name.status_code == HTTPStatus.CONFLICT
    assert response_error_name.json() == {
        'detail': 'Username already exists',
    }

    response_error_email = client.post(
        "/users/",
        json={
            'username': 'VitorinhaGrau',
            'email': 'victor@teste.com',
            'password': 'roubandoemaildomeuirmao',
        }
    )

    assert response_error_email.status_code == HTTPStatus.CONFLICT
    assert response_error_email.json() == {
        'detail': 'Email already exists',
    }


def test_list_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):

    response = client.put(
        '/users/1',
        json={
            'username': 'Victor Mudou',
            'email': 'victor@teste.com',
            'password': 'poncam321',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Victor Mudou',
        'email': 'victor@teste.com',
    }

    response_error = client.put(
        '/users/100',
        json={
            'username': 'Victor Mudou',
            'email': 'victor@teste.com',
            'password': 'poncam321',
        }
    )

    assert response_error.status_code == HTTPStatus.NOT_FOUND
    assert response_error.json() == {
        'detail': 'User not found'
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'pimpolho',
            'email': 'radiotv@fmail.net',
            'password': 'vaicorinthias'
        },
    )

    put_result = client.put(
        f'/users/{user.id}',
        json={
            'username': 'pimpolho',
            'email': 'pimpusmail@gmail.com',
            'password': 'vaicorinthias'
        },
    )

    assert put_result.status_code == HTTPStatus.CONFLICT
    assert put_result.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user):

    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': f'User {user.id} deleted'
    }

    response_error = client.delete('/users/100')

    assert response_error.status_code == HTTPStatus.NOT_FOUND
    assert response_error.json() == {
        'detail': 'User not found'
    }
