from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.data = [
            {"phone_number": "09183385896", "password": "password1"},
            {"phone_number": "09332823692", "password": "password2"},
            {"phone_number": "09125129188", "password": "password3"},
            {"phone_number": "09121125468", "password": "password4"},
        ]
        for i in self.data:
            User.objects.create(**i)

    def validate_number(self, phone_number):
        with self.assertRaises(ValidationError):
            User.objects.create(phone_number=phone_number, password="123456798")

    def test_len_db(self):
        self.assertTrue(User.objects.count(), len(self.data))

    def test_object_manager_soft_delete(self):
        u = User.objects.all().order_by("?").first()
        u.delete()
        self.assertFalse(
            User.objects.count() == len(self.data),
            "Object Manager On Soft Delete Does Not Worked probably",
        )

    def test_validator_phone_number(self):
        self.validate_number("0912111111")
        self.validate_number("0911111111")
        self.validate_number("0900000000")
