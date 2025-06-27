from http import HTTPStatus


def test_hello_world(client):
    # client = TestClient(app)  # Arrange substituido por fixture

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_html(client):
    response = client.get('/hello')

    assert response.status_code == HTTPStatus.OK  # Assert
    assert (
        response.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
    )
