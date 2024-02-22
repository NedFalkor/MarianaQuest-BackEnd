from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from MQ_diving_logs.models.diving_log import DivingLog
from MQ_users.models import CustomUser
from datetime import date


class DivingLogViewSetTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.dive_log_data = {
            'dive_number': 1,
            'dive_date': date.today(),
            'dive_site': 'Test Site',
            'environment': 'sea',
            'depth': 10.0,
            'duration_dive': 30,
        }
        self.dive_log = DivingLog.objects.create(user=self.user, **self.dive_log_data)

    def test_create_diving_log(self):
        url = reverse('divinglog-list')
        response = self.client.post(url, self.dive_log_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DivingLog.objects.count(), 2)

    def test_list_diving_logs(self):
        url = reverse('divinglog-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_diving_log(self):
        url = reverse('divinglog-detail', args=[self.dive_log.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dive_number'], self.dive_log_data['dive_number'])

    def test_update_diving_log(self):
        url = reverse('divinglog-detail', args=[self.dive_log.id])
        updated_data = self.dive_log_data.copy()
        updated_data['dive_site'] = 'Updated Site'
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dive_log.refresh_from_db()
        self.assertEqual(self.dive_log.dive_site, 'Updated Site')

    def test_delete_diving_log(self):
        url = reverse('divinglog-detail', args=[self.dive_log.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DivingLog.objects.count(), 0)

    def tearDown(self):
        self.client.logout()
