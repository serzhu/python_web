import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact, User
from src.schemas import ContactSchema
from src.repository.contacts import (
    get_all_contacts,
    get_contact,
    get_contacts,
    find_contacts,
    find_next_days_birthdays,
    create_contact,
    update_contact,
    delete_contact,
)


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user = User(id=1, username="Test User", email="test@example.com")
        self.contact = Contact(
            id=1,
            name="John",
            surname="Doe",
            email="john.doe@example.com",
            phone="+380951016570",
            birthday=date.today() + timedelta(days=3),
            info="Friend",
            user=self.user,
        )
        self.contact_schema = ContactSchema(
            name="John",
            surname="Doe",
            email="john.doe@example.com",
            phone="+380951016570",
            birthday=date.today() + timedelta(days=3),
            info="Friend",
        )
        self.db = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = [self.contact]
        self.db.execute.return_value = mocked_contacts

        contacts = await get_contacts(10, 0, self.user, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.contact)

    async def test_get_all_contacts(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = [self.contact]
        self.db.execute.return_value = mocked_contacts

        contacts = await get_all_contacts(10, 0, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.contact)

    async def test_get_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.contact
        self.db.execute.return_value = mocked_contact

        contact = await get_contact(1, self.user, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(contact, self.contact)

    async def test_find_contacts_exist(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = [self.contact]
        self.db.execute.return_value = mocked_contacts

        contacts = await find_contacts("John", self.user, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.contact)
        
    async def test_find_contacts_not_exist(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = []
        self.db.execute.return_value = mocked_contacts

        contacts = await find_contacts("Alex", self.user, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(len(contacts), 0)


    async def test_find_next_days_birthdays_exist(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = [self.contact]
        self.db.execute.return_value = mocked_contacts

        contacts = await find_next_days_birthdays(7, self.user, self.db)
        self.db.execute.assert_called_once()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.contact)

    async def test_find_next_days_birthdays_not_exist(self):
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = []
        self.db.execute.return_value = mocked_contacts

        contacts = await find_next_days_birthdays(1, self.user, self.db)
        self.assertEqual(len(contacts), 0)

    async def test_create_contact(self):
        self.db.commit.return_value = None
        self.db.refresh.return_value = None
        self.db.add.return_value = None

        new_contact = await create_contact(self.contact_schema, self.user, self.db)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(new_contact.user, self.user)

    async def test_update_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.contact
        self.db.execute.return_value = mocked_contact
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        updated_contact = await update_contact(1, self.contact_schema, self.user, self.db)
        self.db.execute.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(updated_contact.name, self.contact_schema.name)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = self.contact
        self.db.execute.return_value = mocked_contact
        self.db.commit.return_value = None
        self.db.delete.return_value = None

        deleted_contact = await delete_contact(1, self.user, self.db)
        self.db.execute.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.delete.assert_called_once()
        self.assertEqual(deleted_contact, self.contact)

if __name__ == '__main__':
    unittest.main()