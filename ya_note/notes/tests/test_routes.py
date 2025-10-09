import unittest
from http import HTTPStatus

from .conftest import BaseTestCase


class RouteTests(BaseTestCase):

    def test_anonymous_access(self):
        """Проверка доступа анонимного пользователя к главной странице."""
        response = self.clientSecond.get(
            self.all_urls['general_urls']['notes:home'])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Перенаправление на страницу логина для анонимного пользователя
        urls_anonimus_access = self.all_urls['test_anonymous_access_urls']
        for url in urls_anonimus_access.values():
            response = self.client.get(url)
            self.assertRedirects(
                response,
                f'{self.all_urls['public_urls']['users:login']}?next={url}')

    def test_authenticated_access(self):
        """Проверка доступа к основным страницам и к странице своей заметки."""
        # Проверяем доступ к основным страницам
        urls_authenticated_access = self.all_urls[
            'test_authenticated_access_urls']
        for url in urls_authenticated_access.values():
            with self.subTest():
                response = self.clientFirst.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_public_pages_signup_login_pages(self):
        """Доступность страниц входа и авторизации для всех пользователей."""
        urls = (
            self.all_urls['public_urls']['users:signup'],
            self.all_urls['public_urls']['users:login'])
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_public_pages_logout_page(self):
        """Проверка доступности страницы выхода для всех пользователей."""
        response = self.client.post(self.all_urls['public_urls']['users:logout'])
        self.assertEqual(response.status_code, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
