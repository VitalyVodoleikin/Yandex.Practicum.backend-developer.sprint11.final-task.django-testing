import unittest
from http import HTTPStatus

from django.contrib.auth.models import User
from pytils.translit import slugify

from .conftest import BaseTestCase
from notes.forms import WARNING
from notes.models import Note


class NoteLogicTests(BaseTestCase):

    def test_create_note_authenticated(self):
        """Тест на создание заметки авторизованным пользователем."""
        # Чистим БД
        Note.objects.all().delete()
        # Проверяем, что заметок в БД нет никаких вообще
        self.assertEqual(Note.objects.count(), 0)
        # Создаем заметку
        response = self.client_second.post(
            self.all_urls['general_urls']['notes:add'],
            data={
                'title': self.SECONDUSER_TEST_SECONDNOTE_TITLE,
                'text': self.SECONDUSER_TEST_SECONDNOTE_TEXT})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Проверяем создание новой заметки
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.SECONDUSER_TEST_SECONDNOTE_TITLE)
        self.assertEqual(new_note.text, self.SECONDUSER_TEST_SECONDNOTE_TEXT)
        self.assertEqual(new_note.author, self.user_second_authorized)

    def test_create_note_anonymous(self):
        """Тест на невозможность создания заметки анонимным пользователем."""
        quantity_notes = Note.objects.count()
        response = self.client.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), quantity_notes)

    def test_unique_slug(self):
        """Тест на уникальность slug."""
        quantity_notes = Note.objects.count()
        # Попытка создать заметку с тем же slug
        response = self.client_first.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE,
                'slug': self.first_note_user_first_authorized.slug})
        self.assertEqual(Note.objects.count(), quantity_notes)
        self.assertFormError(
            response.context['form'],
            'slug',
            f'{self.first_note_user_first_authorized.slug}{WARNING}')

    def test_auto_slug(self):
        """Тест на автоматическое формирование slug."""
        Note.objects.all().delete()
        response = self.client_second.post(
            self.all_urls['general_urls']['notes:add'], {
                'title': self.TITLE_NEW_NOTE,
                'text': self.TEXT_NEW_NOTE})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.slug, slugify(self.TITLE_NEW_NOTE))

    def test_edit_own_note(self):
        """Тест на редактирование своей заметки."""
        will_be_edited_note = Note.objects.get(
            id=self.first_note_user_first_authorized.id)
        response = self.client_first.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                'title': self.TITLE_CHANGED_NOTE,
                'text': self.TEXT_CHANGED_NOTE})
        update_note = Note.objects.get(pk=will_be_edited_note.pk)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(update_note.pk, will_be_edited_note.pk)
        self.assertNotEqual(self.TITLE_CHANGED_NOTE, will_be_edited_note.title)
        self.assertNotEqual(self.TEXT_CHANGED_NOTE, will_be_edited_note.text)
        self.assertEqual(update_note.author, will_be_edited_note.author)
        self.assertNotEqual(slugify(self.TITLE_CHANGED_NOTE),
                            will_be_edited_note.slug)
        self.assertEqual(self.TITLE_CHANGED_NOTE, update_note.title)
        self.assertEqual(self.TEXT_CHANGED_NOTE, update_note.text)
        self.assertEqual(slugify(self.TITLE_CHANGED_NOTE), update_note.slug)

    def test_edit_foreign_note(self):
        """Тест на невозможность редактирования чужой заметки."""
        will_be_not_edited_note = Note.objects.get(
            id=self.first_note_user_first_authorized.id)
        response = self.client_second.post(
            self.all_urls['test_authenticated_access_urls']['notes:edit'], {
                'title': self.ATTEMPT_TO_CHAGE_TITLE,
                'text': self.ANOTHER_TEXT_NOTE})
        not_update_note = Note.objects.get(pk=will_be_not_edited_note.pk)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(not_update_note.pk, will_be_not_edited_note.pk)
        self.assertEqual(not_update_note.title, will_be_not_edited_note.title)
        self.assertEqual(not_update_note.text, will_be_not_edited_note.text)
        self.assertEqual(
            not_update_note.author, will_be_not_edited_note.author)
        self.assertEqual(not_update_note.slug, will_be_not_edited_note.slug)

    def test_delete_own_note(self):
        """Тест на удаление своей заметки."""
        quantity_notes = Note.objects.count()
        response = self.client_first.post(
            self.all_urls['test_authenticated_access_urls']['notes:delete'])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), quantity_notes - 1)

    def test_delete_foreign_note(self):
        """Тест на невозможность удаления чужой заметки."""
        # Пытаемся удалить чужую заметку
        response = self.client_second.post(
            self.all_urls['test_anonymous_access_urls']['notes:delete'],
            follow=True)
        # Проверяем, что заметка не была удалена
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(
            id=self.first_note_user_first_authorized.id).exists())


if __name__ == '__main__':
    unittest.main()
