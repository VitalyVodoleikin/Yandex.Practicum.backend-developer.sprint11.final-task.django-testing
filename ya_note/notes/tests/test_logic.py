from http import HTTPStatus
import unittest

from django.contrib.auth.models import User
from pytils.translit import slugify

from .conftest import BaseTestCase
from notes.forms import WARNING
from notes.models import Note


class NoteLogicTests(BaseTestCase):

    def test_create_note_authenticated(self):
        """Тест на создание заметки авторизованным пользователем."""
        # Проверяем начальное количество заметок
        self.assertEqual(Note.objects.count(), self.quantity_notes)
        # Чистим БД
        users_added_notes_in_database = (
            self.userFirstAuthorized,
            self.userSecondAuthorized)
        for user in users_added_notes_in_database:
            user_ = User.objects.get(pk=user.pk)
            Note.objects.filter(author=user_).delete()
        # Создаем заметку
        response = self.clientSecond.post(
            self.all_urls['general_urls']['notes:add'],
            data={
                'title': self.SECONDUSER_TEST_SECONDNOTE_TITLE,
                'text': self.SECONDUSER_TEST_SECONDNOTE_TEXT})
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
        # Чистим БД
        users_added_notes_in_database = (
            self.userFirstAuthorized,
            self.userSecondAuthorized)
        for user in users_added_notes_in_database:
            user_ = User.objects.get(pk=user.pk)
            Note.objects.filter(author=user_).delete()
        response = self.clientSecond.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE})
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
        response = self.clientFirst.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                'title': self.TITLE_CHANGED_NOTE,
                'text': self.TEXT_CHANGED_NOTE})
        update_note = Note.objects.get(pk=will_be_edited_note.pk)
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
        response = self.clientSecond.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                'title': self.ATTEMPT_TO_CHAGE_TITLE,
                'text': self.ANOTHER_TEXT_NOTE})
        not_update_note = Note.objects.get(pk=will_be_not_edited_note.pk)
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
