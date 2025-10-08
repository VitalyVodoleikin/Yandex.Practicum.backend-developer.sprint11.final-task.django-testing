
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from notes.models import Note


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(
            username='UserFirst',
            password='UserFirstPassword')

        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Содержание тестовой заметки',
            author=cls.user)

        cls.url_test_anonymous_access_notes_home = reverse('notes:home')
        cls.url_test_anonymous_access_users_login = reverse('users:login')
        cls.url_test_anonymous_access_users_logout = reverse('users:logout')

        cls.urls_test_anonymous_access = {
            'notes:list': reverse('notes:list'),
            'notes:success': reverse('notes:success'),
            'notes:add': reverse('notes:add'),
            'notes:detail': reverse('notes:detail', args=[cls.note.id]),
            'notes:edit': reverse('notes:edit', args=[cls.note.id]),
            'notes:delete': reverse('notes:delete', args=[cls.note.id])
        }

        cls.urls_test_authenticated_access = {
            'notes:list': reverse('notes:list'),
            'notes:success': reverse('notes:success'),
            'notes:add': reverse('notes:add'),
            'notes:detail': reverse('notes:detail', args=[cls.note.slug]),
            'notes:edit': reverse('notes:edit', args=[cls.note.slug]),
            'notes:delete': reverse('notes:delete', args=[cls.note.slug])
        }

        cls.urls_test_public_pages = {
            'users:signup': reverse('users:signup'),
            'users:login': reverse('users:login'),
            'users:logout': reverse('users:logout')
        }
