from rest_framework.test import APITestCase
from apps.user.models import User
from django.urls import reverse
from rest_framework import status


class APITestCaseBase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='test_email1@neuwerlt.com', password='123pass123',
            username='test1'
        )

        token_url = reverse('token_obtain_pair')
        response = self.client.post(
            token_url,
            {
                'email': 'test_email1@neuwerlt.com',
                'password': '123pass123'
            }
        )

        response = response.json()
        self.assertTrue(response['success'])

        token = response['data']['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
