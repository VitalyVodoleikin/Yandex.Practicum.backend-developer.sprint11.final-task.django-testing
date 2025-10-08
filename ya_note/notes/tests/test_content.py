# Стандартные импорты
import unittest

# Импорты Django (сторонние)
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

# Импорты проекта
from notes.models import Note


class ContentTests(TestCase):

    def setUp(self):
        """Создание тестовых пользователей."""
        self.user1 = User.objects.create_user(
            username='User1',
            password='User1_123')
        self.user2 = User.objects.create_user(
            username='User2',
            password='User2_123')

        """Создание тестовые заметки."""
        self.first_note = Note.objects.create(
            title='Заметка 1',
            text='Содержание заметки 1',
            author=self.user1)
        self.second_note = Note.objects.create(
            title='Заметка 2',
            text='Содержание заметки 2',
            author=self.user2)

        """Создание клиента и авторизация пользователя."""
        self.client = Client()
        self.client.force_login(self.user1)

    def test_note_in_list(self):
        """Проверка передачи заметки в context."""
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.first_note, response.context['object_list'])
        self.assertNotIn(self.second_note, response.context['object_list'])

    def test_user_notes_isolation(self):
        """Проверка изоляции заметок разных пользователей."""
        # Проверка заметок для первого пользователя
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.first_note, response.context['object_list'])
        self.assertNotIn(self.second_note, response.context['object_list'])
        # Авторизация и проверка второго пользователя
        self.client.force_login(self.user2)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.first_note, response.context['object_list'])
        self.assertIn(self.second_note, response.context['object_list'])

    def test_form_in_create_view(self):
        """Проверка передачи формы на страницу создания заметки."""
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

    def test_form_in_edit_view(self):
        """Проверка передачи формы на страницу редактирования заметки."""
        response = self.client.get(reverse(
            'notes:edit', args=[self.first_note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])


if __name__ == '__main__':
    unittest.main()
































# # ----------
# # Стандартные импорты
# import unittest

# # Импорты Django (сторонние)
# from django.contrib.auth.models import User
# from django.test import Client, TestCase
# from django.urls import reverse

# # Импорты проекта
# from notes.models import Note


# class ContentTests(TestCase):

#     def setUp(self):
#         """Создание тестовых пользователей."""
#         self.user1 = User.objects.create_user(
#             username='User1',
#             password='User1_123')
#         self.user2 = User.objects.create_user(
#             username='User2',
#             password='User2_123')

#         """Создание тестовые заметки."""
#         self.first_note = Note.objects.create(
#             title='Заметка 1',
#             text='Содержание заметки 1',
#             author=self.user1)
#         self.second_note = Note.objects.create(
#             title='Заметка 2',
#             text='Содержание заметки 2',
#             author=self.user2)

#         """Создание клиента и авторизация пользователя."""
#         self.client = Client()
#         self.client.force_login(self.user1)

#     def test_note_in_list(self):
#         """Проверка передачи заметки в context."""
#         response = self.client.get(reverse('notes:list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(self.first_note, response.context['object_list'])
#         self.assertNotIn(self.second_note, response.context['object_list'])

#     def test_user_notes_isolation(self):
#         """Проверка изоляции заметок разных пользователей."""
#         # Проверка заметок для первого пользователя
#         response = self.client.get(reverse('notes:list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(self.first_note, response.context['object_list'])
#         self.assertNotIn(self.second_note, response.context['object_list'])
#         # Авторизация и проверка второго пользователя
#         self.client.force_login(self.user2)
#         response = self.client.get(reverse('notes:list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn(self.first_note, response.context['object_list'])
#         self.assertIn(self.second_note, response.context['object_list'])

#     def test_form_in_create_view(self):
#         """Проверка передачи формы на страницу создания заметки."""
#         response = self.client.get(reverse('notes:add'))
#         self.assertEqual(response.status_code, 200)
#         self.assertIsNotNone(response.context['form'])

#     def test_form_in_edit_view(self):
#         """Проверка передачи формы на страницу редактирования заметки."""
#         response = self.client.get(reverse(
#             'notes:edit', args=[self.first_note.slug]))
#         self.assertEqual(response.status_code, 200)
#         self.assertIsNotNone(response.context['form'])


# if __name__ == '__main__':
#     unittest.main()
