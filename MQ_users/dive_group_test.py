from django.test import TestCase
from rest_framework.exceptions import ValidationError

from MQ_users.models import CustomUser
from MQ_users.models.dive_group import DiveGroup


class DiveGroupModelTests(TestCase):

    def setUp(self):
        # This will run before each test in this class
        self.instructor = CustomUser.objects.create(username='instructor', role='INSTRUCTOR')
        self.diver = CustomUser.objects.create(username='diver', role='DIVER')

    def test_dive_group_with_invalid_boat_driver_role(self):
        # Expecting a ValidationError because 'diver' is not an instructor
        with self.assertRaises(ValidationError):
            DiveGroup.objects.create(group_description="Invalid Group", boat_driver=self.diver)

    def test_string_representation(self):
        group = DiveGroup.objects.create(group_description="Cool Dive", boat_driver=self.instructor)
        self.assertEqual(str(group), "Cool Dive")

    def test_get_divers_list(self):
        group = DiveGroup.objects.create(group_description="Dive Group", boat_driver=self.instructor)
        group.divers.add(self.diver)
        self.assertIn(self.diver.username, group.get_divers_list())
