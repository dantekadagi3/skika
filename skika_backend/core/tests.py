from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Report
from rest_framework_simplejwt.tokens import AccessToken
import time

class SkikaBackendTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number="+254712345678", role="citizen", ward="Ward1")
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_user_registration(self):
        data = {'phone_number': '+254712345679', 'role': 'admin', 'ward': 'Ward2'}
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_creation_with_retry(self):
        data = {'ward': 'Ward1', 'category': 'Infrastructure', 'description': 'Road issue'}
        response = self.client.post('/api/reports/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('ref_id' in response.data)

    def test_status_update(self):
        report = Report.objects.create(user=self.user, ref_id="SKK-2025-TEST", ward="Ward1", category="Test", description="Test", status="Received")
        data = {'status': 'Under Review'}
        response = self.client.post(f'/api/reports/{report.id}/update_status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ussd_success_rate(self):
        successes = 0
        total = 10
        for _ in range(total):
            response = self.client.post('/api/reports/ussd_menu/', {'text': '1 Test Issue'}, format='json')
            if response.status_code == status.HTTP_200_OK and "submitted" in response.data['USSResponse']:
                successes += 1
        rate = (successes / total) * 100
        self.assertGreaterEqual(rate, 95)

    def test_concurrent_report_creation(self):
        data = {'ward': 'Ward1', 'category': 'Infrastructure', 'description': 'Concurrent Test'}
        with transaction.atomic():
            responses = [self.client.post('/api/reports/', data, format='json') for _ in range(5)]
            unique_ref_ids = {r.data['ref_id'] for r in responses if r.status_code == status.HTTP_201_CREATED}
            self.assertEqual(len(unique_ref_ids), 1)  # Ensure no duplicates due to transactions

