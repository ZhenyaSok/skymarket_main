from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Ad
from .serializers import AdSerializer


class AdViewSetsTestCase(APITestCase):

    def setUp(self) -> None:

        # Создадим тестовый аккаунт пользователя
        self.user = User.objects.create(email='test@yah.ru', password='123456')
        # Создадим тестовое объявление
        self.ad = Ad.objects.create(title='first ad', author=self.user, price=100, description='test')
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        # self.serializer_ad = AdSerializer([self.ad], many=True).data

    def test_get_queryset_authenticated_user(self):
        url = reverse('ads:ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # serializer_data = AdSerializer([self.ad], many=True).data
        # self.assertEqual(response.data, serializer_data)

    def test_get_queryset_unauthenticated_user(self):
        # Если пользователь не зарегестрирован
        self.client.logout()
        url = reverse('ads:ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_ad(self):
        url = reverse('ads:ads-list')
        data = {
            'title': 'second ad',
            'description': 'test2'
        }
        author = self.user
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ad = Ad.objects.get(title='second ad')
        self.assertEqual(author, ad.author)

    def test_retrieve_ad(self):
        url = reverse('ads:ads-detail', args=[self.ad.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ad(self):
        url = reverse('ads:ads-detail', args=[self.ad.pk])
        data = {
            'title': 'update second ad',
            'description': 'test2'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        val = Ad.objects.get(pk=self.ad.pk)
        self.assertEqual(val.title, 'update second ad')

    def test_delete_ad(self):
        url = reverse('ads:ads-detail', args=[self.ad.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())









