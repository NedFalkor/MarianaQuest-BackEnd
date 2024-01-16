from unittest import TestCase

from MQ_users.models import DiverProfile


class DiverProfileModelTests(TestCase):

    def test_string_representation(self):
        diver = DiverProfile(first_name="John", last_name="Doe")
        self.assertEqual(str(diver), "John Doe")

    def test_diver_creation(self):
        diver = DiverProfile.objects.create(first_name="John", last_name="Doe")
        self.assertTrue(isinstance(diver, DiverProfile))
        self.assertEqual(diver.first_name, "John")
