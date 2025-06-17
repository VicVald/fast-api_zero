from http import HTTPStatus


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


def test_list_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'Victor',
                'email': 'victor@teste.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):

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


def test_delete_user(client):

    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User 1 deleted'
    }

    response_error = client.delete('/users/100')

    assert response_error.status_code == HTTPStatus.NOT_FOUND
    assert response_error.json() == {
        'detail': 'User not found'
    }
