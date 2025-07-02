from http import HTTPStatus

from project.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Victor',
            'email': 'victor@teste.com',
            'password': 'tangerina123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Victor',
        'email': 'victor@teste.com',
        'id': 1,
    }

    response_error_name = client.post(
        '/users/',
        json={
            'username': 'Victor',
            'email': 'victormanjericao@teste.com',
            'password': 'entrandonaconta2918',
        },
    )

    assert response_error_name.status_code == HTTPStatus.CONFLICT
    assert response_error_name.json() == {
        'detail': 'Username already exists',
    }

    response_error_email = client.post(
        '/users/',
        json={
            'username': 'VitorinhaGrau',
            'email': 'victor@teste.com',
            'password': 'roubandoemaildomeuirmao',
        },
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
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Victor Mudou',
        'email': 'victor@teste.com',
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, other_user, token):
    put_result = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'pimpusmail@gmail.com',
            'password': 'vaicorinthias',
        },
    )

    assert put_result.status_code == HTTPStatus.CONFLICT
    assert put_result.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': f'User {user.id} deleted'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
