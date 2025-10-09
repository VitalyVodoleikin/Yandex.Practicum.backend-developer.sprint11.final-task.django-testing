import unittest
from http import HTTPStatus

from notes.forms import NoteForm
from .conftest import BaseTestCase


class ContentTests(BaseTestCase):

    def test_user_note_in_list_and_notes_isolation(self):
        # Проверка передачи заметки в context.
        # Проверка изоляции заметок разных пользователей.
        authenticated_users = (
            (self.client_first, self.first_note_user_first_authorized),
            (self.client_second, self.first_note_user_second_authorized))
        for user, note in authenticated_users:
            with self.subTest(user=user, note=note):
                response = user.get(
                    self.all_urls['general_urls']['notes:list'])
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertIn(note, response.context['object_list'])

    def test_form_in_create_and_edit_view(self):
        # Проверка передачи формы на страницу создания
        # и страницу редактирования заметок.
        urls = (
            self.all_urls['general_urls']['notes:add'],
            self.all_urls['test_authenticated_access_urls']['notes:edit'])
        for url in urls:
            with self.subTest(url=url):
                response = self.client_first.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertIn('form', response.context)
                self.assertIsNotNone(response.context['form'])
                self.assertIsInstance(response.context['form'], NoteForm)


if __name__ == '__main__':
    unittest.main()
