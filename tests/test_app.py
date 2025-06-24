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


def test_update_user(client, user, token):

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Victor Mudou',
            'email': 'victor@teste.com',
            'password': 'poncam321',
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Victor Mudou',
        'email': 'victor@teste.com',
    }


def test_update_integrity_error(client, user, token):
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
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_user(client, user, token):

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': f'User {user.id} deleted'
    }


def test_get_token(user, client):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
