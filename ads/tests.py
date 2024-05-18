from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Ad, Comment
from .serializers import AdSerializer, CommentSerializer


class AdViewSetsTestCase(APITestCase):

    def setUp(self) -> None:

        # Создадим тестовый аккаунт пользователя
        self.user = User.objects.create(email='test@yah.ru', password='123456')
        # Создадим тестовое объявление
        self.ad = Ad.objects.create(title='first ad', author=self.user, price=100, description='test')
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        self.serializer_ad = AdSerializer([self.ad], many=True).data

    def test_get_queryset_authenticated_user(self):
        url = reverse('ads:ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = AdSerializer([self.ad], many=True).data
        self.assertEqual(response.data['results'], serializer_data)
        self.assertEqual(response.json(),
                         {
                             'count': 1,
                             'next': None,
                             'previous': None,
                             'results': [
                                 dict(pk=4, title='first ad', price=100, description='test', image=None,
                                      created_at=response.json()['results'][0]['created_at'])
                             ]
                            })


    def test_get_queryset_unauthenticated_user(self):
        # Если пользователь не зарегестрирован
        self.client.logout()
        url = reverse('ads:ads-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_ad(self):
        """Тест на создание объявления"""
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
        """Тест на редактирование объявления"""
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
        """Тест на удаление объявления"""
        url = reverse('ads:ads-detail', args=[self.ad.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())


class MyAdTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='test@iah.com',
            password='password',
            first_name='test',
            last_name='test'
        )
        self.client.force_authenticate(user=self.user)
    def test_my_ad_list(self):
        """Список объявлений пользователя (личных)"""

        response = self.client.get(reverse('ads:user_ad'),)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})



class CommentViewSetsTestCase(APITestCase):

    def setUp(self) -> None:

        # Создадим тестовый аккаунт пользователя
        self.user = User.objects.create(email='test@yah.ru', password='123456')
        self.user2 = User.objects.create(email='test222@yah.ru', password='123456')
        # Создадим тестовый коммент
        self.ad = Ad.objects.create(title='first ad', author=self.user, price=100, description='test')
        self.comment = Comment.objects.create(text='first comment', author=self.user2, ad=self.ad)
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        self.client.force_authenticate(user=self.user2)
        self.serializer_ad = CommentSerializer([self.comment], many=True).data

    def test_get_queryset_authenticated_user(self):
        url = reverse('ads:comment-list', args=[self.ad.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Comment.objects.all().exists())

    def test_get_queryset_unauthenticated_user(self):
        # Если пользователь не зарегестрирован
        self.client.logout()
        url = reverse('ads:comment-list', args=[self.ad.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review(self):
        """Тестирование создания комментария"""
        data = {
            "text": "Test1",
            "author": self.user.pk,
            "ad": self.ad.pk,
            "created_at": "2021-04-03T09:08:16.430479Z",

        }
        url = reverse('ads:comment-list', args=[self.ad.pk])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.all().exists())

    def test_retrieve_ad(self):

        url = reverse('ads:comment-detail', args=[self.ad.pk, self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ad(self):
        """Тест на редактирование комментария"""
        url = reverse('ads:comment-detail', args=[self.ad.pk, self.comment.pk])
        data = {
            "text": "update second comment",
            "author": self.user.pk,
            "ad": self.ad.pk,
            "created_at": "2021-04-03T09:08:16.430479Z",
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        val = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(val.text, 'update second comment')

    def test_delete_ad(self):
        """Тест на удаление комментария"""
        url = reverse('ads:comment-detail', args=[self.ad.pk, self.comment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())





