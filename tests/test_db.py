from dataclasses import asdict

import pytest
from sqlalchemy import select

from project.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='novo cabeça',
            email='novoemail@terra.com',
            password='gordinhobunitu',
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(
        select(User).where(User.username == 'novo cabeça')
    )

    assert asdict(user) == {
        'id': 1,
        'username': 'novo cabeça',
        'password': 'gordinhobunitu',
        'email': 'novoemail@terra.com',
        'created_at': time,
        'updated_at': time,
    }
