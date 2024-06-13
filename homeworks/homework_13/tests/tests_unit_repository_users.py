import unittest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import User
from src.schemas import UserSchema
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar_url,
)

class TestUserFunctions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User(id=1, username="TestUser", email="test@example.com", avatar=None, refresh_token=None, confirmed=False)
        self.user_schema = UserSchema(
            username="TestUser",
            email="test@example.com",
            password="Hackme12"
        )
        self.db = AsyncMock(spec=AsyncSession)

    async def test_get_user_by_email_exists(self):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.db.execute.return_value = mocked_user

        user = await get_user_by_email("test@example.com", self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(user, self.user)

    async def test_get_user_by_email_not_exists(self):          # Test with no user found
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = None
        self.db.execute.return_value = mocked_user

        user = await get_user_by_email("notfound@example.com", self.db)
        self.db.execute.assert_called_once()
        self.assertIsNone(user)

    async def test_create_user(self):
        self.db.commit.return_value = None
        self.db.refresh.return_value = None
        self.db.add.return_value = None

        new_user = await create_user(self.user_schema, self.db)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(new_user.username, self.user_schema.username)
        self.assertEqual(new_user.email, self.user_schema.email)

    async def test_update_token(self):
        self.db.commit.return_value = None

        await update_token(self.user, "new_refresh_token", self.db)
        self.db.commit.assert_called_once()
        self.assertEqual(self.user.refresh_token, "new_refresh_token")

    async def test_confirmed_email(self):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.db.execute.return_value = mocked_user
        self.db.commit.return_value = None

        await confirmed_email("test@example.com", self.db)
        self.db.execute.assert_called_once()
        self.db.commit.assert_called_once()
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar_url(self):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.db.execute.return_value = mocked_user
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        user = await update_avatar_url("test@example.com", "http://avatar.url", self.db)
        self.db.execute.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(user.avatar, "http://avatar.url")

if __name__ == "__main__":
    unittest.main()
