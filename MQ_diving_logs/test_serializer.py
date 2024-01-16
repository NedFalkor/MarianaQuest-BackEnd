from rest_framework.test import APITestCase
from datetime import date

from MQ_diving_logs.serializers.diving_log_serializer import DivingLogSerializer
from MQ_users.models import CustomUser
from MQ_users.models.dive_group import DiveGroup


class DivingLogSerializerTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.dive_group = DiveGroup.objects.create(group_description="Test Group")
        self.valid_data = {
            'user': self.user.id,
            'dive_number': 1,
            'dive_date': date.today(),
            'dive_group': self.dive_group.id,
        }

    def test_valid_data(self):
        serializer = DivingLogSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['dive_date'] = 'invalid-date'
        serializer = DivingLogSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('dive_date', serializer.errors)
