from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from project.routers import auth, users
from project.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/hello/', response_class=HTMLResponse)
async def show_html():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}
