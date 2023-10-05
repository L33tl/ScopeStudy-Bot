from settings import get_settings
from utils.database.db_worker import DBWorker

import unittest

from utils.database.models.user import User


class TestDBWorker(unittest.TestCase):
    def setUp(self) -> None:
        settings = get_settings('../.env')
        db_path = f'{settings.database.path}/{settings.database.users}'
        self.db_worker = DBWorker(db_path)
        self.db_worker.add_user(1)

    def test_get_user(self):
        self.assertEqual(self.db_worker.get_user(1231232321323121213213231213), None)
        res = self.db_worker.get_user(1)
        self.assertIsInstance(res, User)
        self.assertEqual(res.tg_id, 1)

    def test_add_user(self):
        self.assertEqual(self.db_worker.get_user(2), None)
        self.db_worker.add_user(2)
        user = self.db_worker.get_user(2)
        self.assertIsInstance(user, User)
        self.assertEqual(user.tg_id, 2)
        self.db_worker.remove_user(2)

    def test_update_user_location(self):
        self.assertFalse(self.db_worker.get_user(user_tg_id=1).location)
        self.db_worker.update_user_location(1, (2, 3))
        res = self.db_worker.get_user(1)
        self.assertIsInstance(res, User)
        self.assertEqual(res.location, '2 3')

    def test_remove_user(self):
        self.assertIsNone(self.db_worker.remove_user(123123123123))
        self.db_worker.add_user(2)
        self.assertIsNotNone(self.db_worker.get_user(2))
        self.assertIsNone(self.db_worker.remove_user(2))
        self.assertIsNone(self.db_worker.get_user(2))

    def tearDown(self) -> None:
        self.db_worker.remove_user(1)
