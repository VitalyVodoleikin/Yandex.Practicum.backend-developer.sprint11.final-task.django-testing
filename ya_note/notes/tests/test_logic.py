from http import HTTPStatus
from django.contrib.auth.models import User
import unittest
from notes.models import Note
from pytils.translit import slugify
from .conftest import BaseTestCase
from notes.forms import WARNING


class NoteLogicTests(BaseTestCase):

    def test_create_note_authenticated(self):
        """Тест на создание заметки авторизованным пользователем."""
        # Проверяем начальное количество заметок
        self.assertEqual(Note.objects.count(), self.quantity_notes)
        # print('Кол-во заметок', Note.objects.count())

        # Чистим БД
        users_added_notes_in_database = (
            self.userFirstAuthorized,
            self.userSecondAuthorized
        )

        for user in users_added_notes_in_database:
            user_ = User.objects.get(pk=user.pk)
            Note.objects.filter(author=user_).delete()

        # print('БД очищена')
        # print('Кол-во заметок', Note.objects.count())

        # Создаем заметку
        response = self.clientSecond.post(
            self.all_urls['general_urls']['notes:add'],
            data={
                'title': self.SECONDUSER_TEST_SECONDNOTE_TITLE,
                'text': self.SECONDUSER_TEST_SECONDNOTE_TEXT})
        
        # print('В БД добавлена 1 заметка')
        # print('Кол-во заметок', Note.objects.count())
        
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Проверяем создание новой заметки
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.SECONDUSER_TEST_SECONDNOTE_TITLE)
        self.assertEqual(new_note.text, self.SECONDUSER_TEST_SECONDNOTE_TEXT)
        self.assertEqual(new_note.author, self.userSecondAuthorized)

    def test_create_note_anonymous(self):
        """Тест на невозможность создания заметки анонимным пользователем."""
        response = self.clientThirdAnonimus.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), self.quantity_notes)

    def test_unique_slug(self):
        """Тест на уникальность slug."""
        # Попытка создать заметку с тем же slug
        response = self.clientFirst.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE,
                'slug': self.first_note_userFirstAuthorized.slug})
        self.assertEqual(Note.objects.count(), self.quantity_notes)
        self.assertFormError(
            response.context['form'],
            'slug',
            f'{self.first_note_userFirstAuthorized.slug}{WARNING}')

    def test_auto_slug(self):
        """Тест на автоматическое формирование slug."""

        # Проверяем начальное количество заметок
        self.assertEqual(Note.objects.count(), self.quantity_notes)
        # print('Кол-во заметок', Note.objects.count())

        # Чистим БД
        users_added_notes_in_database = (
            self.userFirstAuthorized,
            self.userSecondAuthorized
        )

        for user in users_added_notes_in_database:
            user_ = User.objects.get(pk=user.pk)
            Note.objects.filter(author=user_).delete()

        # print('БД очищена')
        # print('Кол-во заметок', Note.objects.count())

        response = self.clientSecond.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE})
        
        # print('В БД добавлена 1 заметка')
        # print('Кол-во заметок', Note.objects.count())

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        new_note = Note.objects.get()
        self.assertEqual(new_note.slug, slugify(self.TITLE_NEW_NOTE))

    def test_edit_own_note(self):
        """Тест на редактирование своей заметки."""

        will_be_edited_note = Note.objects.get(
            id=self.first_note_userFirstAuthorized.id)

        original_pk = will_be_edited_note.pk
        original_title = will_be_edited_note.title
        original_text = will_be_edited_note.text
        original_author = will_be_edited_note.author
        original_slug = will_be_edited_note.slug

        # print('-' * 30)
        # print(original_pk)
        # print(original_title)
        # print(original_text)
        # print(original_author)
        # print(original_slug)
        # print('-' * 30)

        response = self.clientFirst.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                # 'pk': self.first_note_userFirstAuthorized.pk,
                'title': self.TITLE_CHANGED_NOTE,
                'text': self.TEXT_CHANGED_NOTE})

        update_note = Note.objects.get(pk=will_be_edited_note.pk)

        # print('-' * 30)
        # print(update_note.pk)
        # print(update_note.title)
        # print(update_note.text)
        # print(update_note.author)
        # print(update_note.slug)
        # print('-' * 30)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(update_note.pk, original_pk)
        self.assertNotEqual(update_note.title, original_title)
        self.assertNotEqual(update_note.text, original_text)
        self.assertEqual(update_note.author, original_author)
        self.assertNotEqual(update_note.slug, original_slug)

    def test_edit_foreign_note(self):
        """Тест на невозможность редактирования чужой заметки."""

        will_be_not_edited_note = Note.objects.get(
            id=self.first_note_userFirstAuthorized.id)

        original_pk = will_be_not_edited_note.pk
        original_title = will_be_not_edited_note.title
        original_text = will_be_not_edited_note.text
        original_author = will_be_not_edited_note.author
        original_slug = will_be_not_edited_note.slug

        # print('-' * 30)
        # print(original_pk)
        # print(original_title)
        # print(original_text)
        # print(original_author)
        # print(original_slug)
        # print('-' * 30)

        response = self.clientSecond.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                # 'pk': self.first_note_userFirstAuthorized.pk,
                'title': self.ATTEMPT_TO_CHAGE_TITLE,
                'text': self.ANOTHER_TEXT_NOTE})
        
        not_update_note = Note.objects.get(pk=will_be_not_edited_note.pk)

        # print('-' * 30)
        # print(not_update_note.pk)
        # print(not_update_note.title)
        # print(not_update_note.text)
        # print(not_update_note.author)
        # print(not_update_note.slug)
        # print('-' * 30)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(not_update_note.pk, original_pk)
        self.assertEqual(not_update_note.title, original_title)
        self.assertEqual(not_update_note.text, original_text)
        self.assertEqual(not_update_note.author, original_author)
        self.assertEqual(not_update_note.slug, original_slug)

    def test_delete_own_note(self):
        """Тест на удаление своей заметки."""
        response = self.clientFirst.post(
            self.all_urls['test_authenticated_access_urls']['notes:delete'])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), self.quantity_notes - 1)

    def test_delete_foreign_note(self):
        """Тест на невозможность удаления чужой заметки."""
        # Пытаемся удалить чужую заметку
        response = self.clientSecond.post(
            self.all_urls['test_anonymous_access_urls']['notes:delete'],
            follow=True)
        # Проверяем, что заметка не была удалена
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(
            id=self.first_note_userFirstAuthorized.id).exists())


if __name__ == '__main__':
    unittest.main()







# +++













# # ---------
# import unittest
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.test import Client, TestCase
# from notes.models import Note
# from pytils.translit import slugify


# class NoteLogicTests(TestCase):

#     def setUp(self):
#         """Создание тестовых пользователей."""
#         self.user1 = User.objects.create_user(
#             username='User1', password='User1_123')
#         self.user2 = User.objects.create_user(
#             username='User2', password='User2_123')

#         """Создание клиента и авторизация пользователя."""
#         self.client = Client()
#         self.client.force_login(self.user1)

#         """Создание тестовую заметку."""
#         self.note = Note.objects.create(
#             title='Тест',
#             text='Содержание теста',
#             author=self.user1)

#     def test_create_note_authenticated(self):
#         """Тест на создание заметки авторизованным пользователем."""
#         # Проверяем начальное количество заметок
#         self.assertEqual(Note.objects.count(), 1)
#         response = self.client.post(reverse('notes:add'), data={
#             'title': 'Новая заметка',
#             'text': 'Содержание новой заметки'})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Note.objects.count(), 2)
#         # Проверяем создание новой заметки
#         new_note = Note.objects.last()
#         self.assertEqual(new_note.title, 'Новая заметка')
#         self.assertEqual(new_note.text, 'Содержание новой заметки')
#         self.assertEqual(new_note.author, self.user1)
#         # print('Good')

#     def test_create_note_anonymous(self):
#         """Тест на невозможность создания заметки анонимным пользователем."""
#         anon_client = Client()
#         response = anon_client.post(reverse('notes:add'), {
#             'title': 'Новая заметка',
#             'text': 'Содержание новой заметки'})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Note.objects.count(), 1)

#     def test_unique_slug(self):
#         """Тест на уникальность slug."""
#         # Попытка создать заметку с тем же slug
#         with self.assertRaises(Exception):
#             Note.objects.create(
#                 title=self.note.title,
#                 text='Другое содержание',
#                 author=self.user1,
#                 slug=self.note.slug)

#     def test_auto_slug(self):
#         """Тест на автоматическое формирование slug."""
#         response = self.client.post(reverse('notes:add'), {
#             'title': 'Тестовая заметка',
#             'text': 'Содержание'})
#         self.assertEqual(response.status_code, 302)
#         new_note = Note.objects.last()
#         self.assertEqual(new_note.slug, slugify('тестовая-заметка'))

#     def test_edit_own_note(self):
#         """Тест на редактирование своей заметки."""
#         response = self.client.post(reverse(
#             'notes:edit', args=[self.note.slug]), {
#             'title': 'Измененная заметка',
#             'text': 'Новое содержание'})
#         self.assertEqual(response.status_code, 302)
#         self.note.refresh_from_db()
#         self.assertEqual(self.note.title, 'Измененная заметка')

#     def test_edit_foreign_note(self):
#         """Тест на невозможность редактирования чужой заметки."""
#         # Создаем заметку для второго пользователя
#         foreign_note = Note.objects.create(
#             title='Чужая заметка',
#             text='Содержание чужой заметки',
#             author=self.user2)
#         response = self.client.post(reverse(
#             'notes:edit', args=[foreign_note.slug]), {
#             'title': 'Попытка изменения'})
#         self.assertEqual(response.status_code, 404)  # Запрещено

#     def test_delete_own_note(self):
#         """Тест на удаление своей заметки."""
#         response = self.client.post(reverse(
#             'notes:delete', args=[self.note.slug]))
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Note.objects.count(), 0)

#     def test_delete_foreign_note(self):
#         """Тест на невозможность удаления чужой заметки."""
#         # Создаем заметку для второго пользователя
#         foreign_note = Note.objects.create(
#             title='Чужая заметка',
#             text='Содержание чужой заметки',
#             author=self.user2)  # Указываем автора заметки
#         # Авторизуем первого пользователя
#         self.client.force_login(self.user1)
#         # Пытаемся удалить чужую заметку
#         response = self.client.post(
#             reverse('notes:delete', args=[foreign_note.id]),
#             follow=True)
#         # Проверяем, что заметка не была удалена
#         self.assertEqual(response.status_code, 404)
#         self.assertTrue(Note.objects.filter(id=foreign_note.id).exists())


# if __name__ == '__main__':
#     unittest.main()
