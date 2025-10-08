import unittest
from http import HTTPStatus, client
from .conftest import BaseTestCase


class RouteTests(BaseTestCase):

    def setUp(self):
        super().setUpTestData()
        self.client = client()
        self.client.force_login(self.user)

    def test_anonymous_access(self):
        """Проверка доступа анонимного пользователя к главной странице."""
        response = self.client.get(self.url_test_anonymous_access_notes_home)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Перенаправление на страницу логина для анонимного пользователя
        urls_anonimus_access = self.urls_test_anonymous_access
        for url in urls_anonimus_access.values():
            response = self.client.get(url)
            self.assertRedirects(
                response,
                f'{self.url_test_anonymous_access_users_login}?next={url}'
            )

    def test_authenticated_access(self):
        """Проверка доступа к основным страницам и к странице своей заметки."""
        # # Авторизуем пользователя
        # self.client.login(username='User1', password='User1password')
        # Проверяем доступ к основным страницам
        urls_authenticated_access = self.urls_test_authenticated_access
        for url in urls_authenticated_access.values():
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_public_pages_signup_login_pages(self):
        """Доступность страниц входа и авторизации для всех пользователей."""
        urls = (
            self.urls_test_public_pages['users:signup'],
            self.urls_test_public_pages['users:login']
        )
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_public_pages_logout_page(self):
        """Проверка доступности страницы выхода для всех пользователей."""
        response = self.client.post(self.urls_test_public_pages['users:logout'])
        self.assertEqual(response.status_code, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()














# # ----------
# import unittest
# from django.contrib.auth.models import User
# from django.urls import reverse
# from django.test import TestCase, Client
# from notes.models import Note


# class RouteTests(TestCase):
#     def setUp(self):
#         """Создание тестового пользователя."""
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='User1',
#             password='User1password')
#         self.note = Note.objects.create(
#             title='Тестовая заметка',
#             text='Содержание тестовой заметки',
#             author=self.user)

#     def test_anonymous_access(self):
#         """Проверка доступа анонимного пользователя к главной странице."""
#         response = self.client.get(reverse('notes:home'))
#         self.assertEqual(response.status_code, 200)
#         # Перенаправление на страницу логина для анонимного пользователя
#         urls = [
#             reverse('notes:list'),
#             reverse('notes:success'),
#             reverse('notes:add'),
#             reverse('notes:detail', args=[self.note.id]),
#             reverse('notes:edit', args=[self.note.id]),
#             reverse('notes:delete', args=[self.note.id]),]
#         for url in urls:
#             login_url = reverse('users:login')
#             response = self.client.get(url)
#             self.assertRedirects(response, f'{login_url}?next={url}')

#     def test_authenticated_access(self):
#         """Проверка доступа к основным страницам и к странице своей заметки."""
#         # Авторизуем пользователя
#         self.client.login(username='User1', password='User1password')
#         # Проверяем доступ к основным страницам
#         response = self.client.get(reverse('notes:list'))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse('notes:success'))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse('notes:add'))
#         self.assertEqual(response.status_code, 200)
#         # Проверяем доступ к странице своей заметки
#         response = self.client.get(reverse(
#             'notes:detail', args=[self.note.slug]))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse(
#             'notes:edit', args=[self.note.slug]))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse(
#             'notes:delete', args=[self.note.slug]))
#         self.assertEqual(response.status_code, 200)

#     def test_public_pages(self):
#         """Проверка доступности публичных страниц для всех пользователей."""
#         public_urls = [
#             reverse('users:signup'),
#             reverse('users:login'),
#             reverse('users:logout'),]
#         for url in public_urls:
#             if url == reverse('users:logout'):
#                 response = self.client.post(url)
#             else:
#                 response = self.client.get(url)
#             self.assertEqual(response.status_code, 200)


# if __name__ == '__main__':
#     unittest.main()
