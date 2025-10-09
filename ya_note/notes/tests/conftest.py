from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Создание первого авторизованного пользователя
        cls.userFirstAuthorized = User.objects.create_user(
            username='UserFirstAuthorized',
            password='UserFirstAuthorizedPassword')

        cls.clientFirst = Client()
        cls.clientFirst.force_login(cls.userFirstAuthorized)
      
        # Создание первой заметки первого авторизованного пользователя
        cls.first_note_userFirstAuthorized = Note.objects.create(
            title='Тестовая заметка 1 авторизованного пользователя 1',
            text='Содержание заметки 1 авторизованного пользователя 1',
            author=cls.userFirstAuthorized)

        cls.url_test_anonymous_access_notes_home = reverse('notes:home')
        cls.url_test_anonymous_access_users_login = reverse('users:login')
        cls.url_test_anonymous_access_users_logout = reverse('users:logout')

        cls.urls_test_anonymous_access = {
            'notes:list': reverse('notes:list'),
            'notes:success': reverse('notes:success'),
            'notes:add': reverse('notes:add'),
            'notes:detail': reverse('notes:detail', args=[cls.first_note_userFirstAuthorized.id]),
            'notes:edit': reverse('notes:edit', args=[cls.first_note_userFirstAuthorized.id]),
            'notes:delete': reverse('notes:delete', args=[cls.first_note_userFirstAuthorized.id])
        }

        cls.urls_test_authenticated_access = {
            'notes:list': reverse('notes:list'),
            'notes:success': reverse('notes:success'),
            'notes:add': reverse('notes:add'),
            'notes:detail': reverse('notes:detail', args=[cls.first_note_userFirstAuthorized.slug]),
            'notes:edit': reverse('notes:edit', args=[cls.first_note_userFirstAuthorized.slug]),
            'notes:delete': reverse('notes:delete', args=[cls.first_note_userFirstAuthorized.slug])
        }

        cls.urls_test_public_pages = {
            'users:signup': reverse('users:signup'),
            'users:login': reverse('users:login'),
            'users:logout': reverse('users:logout')
        }

        cls.SECOND_TEST_NOTE_TITLE = 'Тестовая заметка 2 авторизованного пользователя 2'
        cls.SECOND_TEST_NOTE_TEXT = 'Содержание заметки 2 авторизованного пользователя 2'
        cls.TITLE_CHANGED_NOTE = 'Измененная заметка'
        cls.TEXT_CHANGED_NOTE = 'Новое содержание измененной заметки'
        cls.TITLE_NEW_NOTE = 'Новая заметка'
        cls.TEXT_NEW_NOTE = 'Содержание новой заметки'
        cls.ANOTHER_TEXT_NOTE = 'Другое содержание'
        cls.ATTEMPT_TO_CHAGE = 'Попытка изменения'

    def setUp(self):

        # Создание второго авторизованного пользователя
        self.userSecondAuthorized = User.objects.create_user(
            username='UserSecond',
            password='UserSecondPassword'
        )
        self.clientSecond = Client()
        self.clientSecond.force_login(self.userSecondAuthorized)

        # Создание третьего неавторизованного пользователя (Аноним)
        self.clientThirdAnonimus = Client()

        # Создание второй заметки второго авторизованного пользователя
        self.second_note_userSecondAuthorized = Note.objects.create(
            title='Тестовая заметка 1 авторизованного пользователя 2',
            text='Содержание заметки 1 авторизованного пользователя 2',
            author=self.userSecondAuthorized)

        self.quantity_notes = Note.objects.count()















# # ----------++++++++++----------
# from django.contrib.auth.models import User
# from django.test import Client, TestCase
# from django.urls import reverse
# from notes.models import Note


# class BaseTestCase(TestCase):

#     @classmethod
#     def setUpTestData(cls):

#         # Создание первого авторизованного пользователя
#         cls.userFirstAuthorized = User.objects.create_user(
#             username='UserFirstAuthorized',
#             password='UserFirstAuthorizedPassword')

#         cls.clientFirst = Client()
#         cls.clientFirst.force_login(cls.userFirstAuthorized)
      
#         # Создание первой заметки первого авторизованного пользователя
#         cls.first_note_userFirstAuthorized = Note.objects.create(
#             title='Тестовая заметка 1 авторизованного пользователя 1',
#             text='Содержание тестовой заметки 1 авторизованного пользователя 1',
#             author=cls.userFirstAuthorized)

#         cls.url_test_anonymous_access_notes_home = reverse('notes:home')
#         cls.url_test_anonymous_access_users_login = reverse('users:login')
#         cls.url_test_anonymous_access_users_logout = reverse('users:logout')

#         cls.urls_test_anonymous_access = {
#             'notes:list': reverse('notes:list'),
#             'notes:success': reverse('notes:success'),
#             'notes:add': reverse('notes:add'),
#             'notes:detail': reverse('notes:detail', args=[cls.first_note_userFirstAuthorized.id]),
#             'notes:edit': reverse('notes:edit', args=[cls.first_note_userFirstAuthorized.id]),
#             'notes:delete': reverse('notes:delete', args=[cls.first_note_userFirstAuthorized.id])
#         }

#         cls.urls_test_authenticated_access = {
#             'notes:list': reverse('notes:list'),
#             'notes:success': reverse('notes:success'),
#             'notes:add': reverse('notes:add'),
#             'notes:detail': reverse('notes:detail', args=[cls.first_note_userFirstAuthorized.slug]),
#             'notes:edit': reverse('notes:edit', args=[cls.first_note_userFirstAuthorized.slug]),
#             'notes:delete': reverse('notes:delete', args=[cls.first_note_userFirstAuthorized.slug])
#         }

#         cls.urls_test_public_pages = {
#             'users:signup': reverse('users:signup'),
#             'users:login': reverse('users:login'),
#             'users:logout': reverse('users:logout')
#         }

#     def setUp(self):

#         # Создание второго авторизованного пользователя
#         self.userSecondAuthorized = User.objects.create_user(
#             username='UserSecond',
#             password='UserSecondPassword'
#         )
#         self.clientSecond = Client()
#         self.clientSecond.force_login(self.userSecondAuthorized)

#         # Создание третьего неавторизованного пользователя (Аноним)
#         self.clientThirdAnonimus = Client()

#         # Создание второй заметки второго авторизованного пользователя
#         self.second_note_userSecondAuthorized = Note.objects.create(
#             title='Тестовая заметка 1 авторизованного пользователя 2',
#             text='Содержание тестовой заметки 1 авторизованного пользователя 2',
#             author=self.userSecondAuthorized)
        



# # ----------
# from django.contrib.auth.models import User

# from django.test import Client, TestCase
# from django.urls import reverse

# from notes.models import Note


# class BaseTestCase(TestCase):

#     @classmethod
#     def setUpTestData(cls):
        
#         cls.userFirst = User.objects.create_user(
#             username='UserFirst',
#             password='UserFirstpassword')
        
#         cls.clientFirst = Client()
#         cls.clientFirst.force_login(cls.userFirst)
                
#         cls.note = Note.objects.create(
#             title='Тестовая заметка',
#             text='Содержание тестовой заметки',
#             author=cls.userFirst)

#         cls.url_test_anonymous_access_notes_home = reverse('notes:home')
#         cls.url_test_anonymous_access_users_login = reverse('users:login')
#         cls.url_test_anonymous_access_users_logout = reverse('users:logout')

#         cls.urls_test_anonymous_access = {
#             'notes:list': reverse('notes:list'),
#             'notes:success': reverse('notes:success'),
#             'notes:add': reverse('notes:add'),
#             'notes:detail': reverse('notes:detail', args=[cls.note.id]),
#             'notes:edit': reverse('notes:edit', args=[cls.note.id]),
#             'notes:delete': reverse('notes:delete', args=[cls.note.id])
#         }

#         cls.urls_test_authenticated_access = {
#             'notes:list': reverse('notes:list'),
#             'notes:success': reverse('notes:success'),
#             'notes:add': reverse('notes:add'),
#             'notes:detail': reverse('notes:detail', args=[cls.note.slug]),
#             'notes:edit': reverse('notes:edit', args=[cls.note.slug]),
#             'notes:delete': reverse('notes:delete', args=[cls.note.slug])
#         }

#         cls.urls_test_public_pages = {
#             'users:signup': reverse('users:signup'),
#             'users:login': reverse('users:login'),
#             'users:logout': reverse('users:logout')
#         }

#     def setUp(self):

#         self.userSecond = User.objects.create_user(
#             username='UserSecond',
#             password='UserSecondPassword'
#         )

#         self.clientSecond = Client()
#         self.clientSecond.force_login(self.userSecond)
