from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Создание первого пользователя
        cls.user_first_authorized = User.objects.create_user(
            username='user_first_authorized',
            password='user_first_authorizedPassword')

        # Создание второго авторизованного пользователя
        cls.user_second_authorized = User.objects.create_user(
            username='UserSecond',
            password='UserSecondPassword')

        # Авторизация первого и второго пользователей
        cls.client_first = Client()
        cls.client_first.force_login(cls.user_first_authorized)
        cls.client_second = Client()
        cls.client_second.force_login(cls.user_second_authorized)

        # Создание первой заметки первого авторизованного пользователя
        cls.first_note_user_first_authorized = Note.objects.create(
            title='Тестовая заметка 1 авториз. пользователя 1',
            text='Содержание заметки 1 авториз. пользователя 1',
            author=cls.user_first_authorized)

        # Создание второй заметки второго авторизованного пользователя
        cls.first_note_user_second_authorized = Note.objects.create(
            title='Тестовая заметка 1 авториз. пользователя 2',
            text='Содержание заметки 1 авториз. пользователя 2',
            author=cls.user_second_authorized)

        # Маршруты
        cls.all_urls = {
            'general_urls': {
                'notes:home': reverse('notes:home'),
                'notes:list': reverse('notes:list'),
                'notes:success': reverse('notes:success'),
                'notes:add': reverse('notes:add')},

            'public_urls': {
                'users:signup': reverse('users:signup'),
                'users:login': reverse('users:login'),
                'users:logout': reverse('users:logout')},

            'test_anonymous_access_urls': {
                'notes:detail': reverse(
                    'notes:detail',
                    args=[cls.first_note_user_first_authorized.id]),
                'notes:edit': reverse(
                    'notes:edit',
                    args=[cls.first_note_user_first_authorized.id]),
                'notes:delete': reverse(
                    'notes:delete',
                    args=[cls.first_note_user_first_authorized.id])},

            'test_authenticated_access_urls': {
                'notes:detail': reverse(
                    'notes:detail',
                    args=[cls.first_note_user_first_authorized.slug]),
                'notes:edit': reverse(
                    'notes:edit',
                    args=[cls.first_note_user_first_authorized.slug]),
                'notes:delete': reverse(
                    'notes:delete',
                    args=[cls.first_note_user_first_authorized.slug])}}

        # Константы
        cls.ANOTHER_TEXT_NOTE = 'Другое содержание'
        cls.ATTEMPT_TO_CHAGE_TITLE = 'Попытка изменения'

        cls.TITLE_NEW_NOTE = 'Новая заметка'
        cls.TEXT_NEW_NOTE = 'Содержание новой заметки'

        cls.TITLE_CHANGED_NOTE = 'Измененная заметка'
        cls.TEXT_CHANGED_NOTE = 'Новое содержание измененной заметки'

        cls.SECONDUSER_TEST_SECONDNOTE_TITLE = 'Заметка 2 авториз. польз-ля 2'
        cls.SECONDUSER_TEST_SECONDNOTE_TEXT = 'Заметка_ 2 авториз. польз-ля 2'
