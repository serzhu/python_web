## Tests

Added folder test with some tests:<br />
- testing all functions in repository/users with unittest
```bash
python -m tests.tests_unit_repository_users
```
- testing all functions in repository/contacts
```bash
python -m tests.tests_unit_repository_contacts
```
- testing all functions in routes/contacts
```bash
python -m pytest ./tests/tests_route_contacts.py -v
```
