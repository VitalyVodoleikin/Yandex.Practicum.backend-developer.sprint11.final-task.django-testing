from http import HTTPStatus
import pytest

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from news.models import Comment, News
from .conftest import (
    another_user_client, detail_url, home_url
)

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestRoutes:


    @pytest.mark.parametrize(
            ['reverse_url', 'parametrized_client', 'status'],
            [
                (home_url, another_user_client, HTTPStatus.OK),
                (detail_url, another_user_client, HTTPStatus.OK),
            ]
    )
    def test_status_codes(self, reverse_url, parametrized_client, status):
        # запрос
        response = parametrized_client.get(reverse_url)
        # ассерт
        assert response.status_code == status



    # # Тесты для анонимного пользователя
    # def test_anonymous_home_page(self, another_user_client, home_url):
    #     response = another_user_client.get(home_url)
    #     assert response.status_code == HTTPStatus.OK

    # def test_anonymous_news_detail(self, another_user_client, detail_url):
    #     response = another_user_client.get(detail_url)
    #     assert response.status_code == HTTPStatus.OK

    # def test_anonymous_comment_edit_redirect(self, another_user_client,
    #                                          login_url, edit_url):
    #     response = another_user_client.get(edit_url)
    #     if response.status_code == HTTPStatus.NOT_FOUND:
    #         assert True
    #     else:
    #         assert response.status_code == HTTPStatus.FOUND
    #         assert response.url == f'{login_url}?next={edit_url}'

    # def test_anonymous_comment_delete_redirect(self, another_user_client,
    #                                            login_url, delete_url):
    #     response = another_user_client.get(delete_url)
    #     if response.status_code == HTTPStatus.NOT_FOUND:
    #         assert True
    #     else:
    #         assert response.status_code == HTTPStatus.FOUND
    #         assert response.url == f'{login_url}?next={delete_url}'

    # def test_anonymous_auth_pages(self, another_user_client, login_url,
    #                               signup_url, logout_url):
    #     login_response = another_user_client.get(login_url)
    #     assert login_response.status_code == HTTPStatus.OK
    #     signup_response = another_user_client.get(signup_url)
    #     assert signup_response.status_code == HTTPStatus.OK
    #     logout_response = another_user_client.post(logout_url)
    #     assert logout_response.status_code == HTTPStatus.OK






    # # Тесты для авторизованного пользователя
    # def test_authorized_comment_edit(self, author_client, edit_url):
    #     response = author_client.get(edit_url)
    #     assert response.status_code == HTTPStatus.OK

    # def test_authorized_comment_delete(self, author_client, delete_url):
    #     response = author_client.get(delete_url)
    #     assert response.status_code == HTTPStatus.OK

    # def test_authorized_foreign_comment_edit(self, author_client,
    #                                          foreign_edit_url):
    #     response = author_client.get(foreign_edit_url)
    #     assert response.status_code == HTTPStatus.NOT_FOUND

    # def test_authorized_foreign_comment_delete(self, author_client,
    #                                            foreign_delete_url):
    #     response = author_client.get(foreign_delete_url)
    #     assert response.status_code == HTTPStatus.NOT_FOUND









# # ==========++++++++++==========
# from http import HTTPStatus
# import pytest

# from django.contrib.auth import get_user_model
# from django.test import Client
# from django.urls import reverse

# from news.models import Comment, News

# User = get_user_model()

# pytestmark = pytest.mark.django_db


# class TestRoutes:

#     # Тесты для анонимного пользователя
#     def test_anonymous_home_page(self, another_user_client, home_url):
#         response = another_user_client.get(home_url)
#         assert response.status_code == HTTPStatus.OK

#     def test_anonymous_news_detail(self, another_user_client, detail_url):
#         response = another_user_client.get(detail_url)
#         assert response.status_code == HTTPStatus.OK

#     def test_anonymous_comment_edit_redirect(self, another_user_client,
#                                              login_url, edit_url):
#         response = another_user_client.get(edit_url)
#         if response.status_code == HTTPStatus.NOT_FOUND:
#             assert True
#         else:
#             assert response.status_code == HTTPStatus.FOUND
#             assert response.url == f'{login_url}?next={edit_url}'

#     def test_anonymous_comment_delete_redirect(self, another_user_client,
#                                                login_url, delete_url):
#         response = another_user_client.get(delete_url)
#         if response.status_code == HTTPStatus.NOT_FOUND:
#             assert True
#         else:
#             assert response.status_code == HTTPStatus.FOUND
#             assert response.url == f'{login_url}?next={delete_url}'

#     def test_anonymous_auth_pages(self, another_user_client, login_url,
#                                   signup_url, logout_url):
#         login_response = another_user_client.get(login_url)
#         assert login_response.status_code == HTTPStatus.OK
#         signup_response = another_user_client.get(signup_url)
#         assert signup_response.status_code == HTTPStatus.OK
#         logout_response = another_user_client.post(logout_url)
#         assert logout_response.status_code == HTTPStatus.OK

#     # Тесты для авторизованного пользователя
#     def test_authorized_comment_edit(self, author_client, edit_url):
#         response = author_client.get(edit_url)
#         assert response.status_code == HTTPStatus.OK

#     def test_authorized_comment_delete(self, author_client, delete_url):
#         response = author_client.get(delete_url)
#         assert response.status_code == HTTPStatus.OK

#     def test_authorized_foreign_comment_edit(self, author_client,
#                                              foreign_edit_url):
#         response = author_client.get(foreign_edit_url)
#         assert response.status_code == HTTPStatus.NOT_FOUND

#     def test_authorized_foreign_comment_delete(self, author_client,
#                                                foreign_delete_url):
#         response = author_client.get(foreign_delete_url)
#         assert response.status_code == HTTPStatus.NOT_FOUND



# # ==========
# from http import HTTPStatus
# import pytest

# from django.contrib.auth import get_user_model
# from django.test import Client
# from django.urls import reverse

# from news.models import Comment, News

# User = get_user_model()

# pytestmark = pytest.mark.django_db


# class TestRoutes:

#     @pytest.fixture(autouse=True)
#     def setup(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='User1',
#             password='User1password',
#             is_active=True
#         )
#         self.news = News.objects.create(
#             title='Test News',
#             text='Content of the test news'
#         )
#         self.comment = Comment.objects.create(
#             news=self.news,
#             author=self.user,
#             text='Test comment'
#         )

#     # Тесты для анонимного пользователя
#     def test_anonymous_home_page(self):
#         response = self.client.get(reverse('news:home'))
#         assert response.status_code == HTTPStatus.OK

#     def test_anonymous_news_detail(self):
#         response = self.client.get(reverse('news:detail', args=[self.news.id]))
#         assert response.status_code == HTTPStatus.OK

#     def test_anonymous_comment_edit_redirect(self):
#         url_login = reverse('users:login')
#         response = self.client.get(reverse('news:edit', args=[self.comment.id]))
#         assert response.status_code == HTTPStatus.FOUND
#         assert response.url == f'{url_login}?next={reverse('news:edit', args=[self.comment.id])}'

#     def test_anonymous_comment_delete_redirect(self):
#         url_login = reverse('users:login')
#         response = self.client.get(reverse('news:delete', args=[self.comment.id]))
#         assert response.status_code == HTTPStatus.FOUND
#         assert response.url == f'{url_login}?next={reverse('news:delete', args=[self.comment.id])}'

#     def test_anonymous_auth_pages(self):
#         login_response = self.client.get(reverse('users:login'))
#         assert login_response.status_code == HTTPStatus.OK
#         signup_response = self.client.get(reverse('users:signup'))
#         assert signup_response.status_code == HTTPStatus.OK
#         logout_response = self.client.post(reverse('users:logout'))
#         assert logout_response.status_code == HTTPStatus.OK

#     # Тесты для авторизованного пользователя
#     def test_authorized_comment_edit(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('news:edit', args=[self.comment.id]))
#         assert response.status_code == HTTPStatus.OK

#     def test_authorized_comment_delete(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('news:delete', args=[self.comment.id]))
#         assert response.status_code == HTTPStatus.OK

#     def test_authorized_foreign_comment_edit(self):
#         other_user = User.objects.create_user(
#             username='anotheruser',
#             password='anotherpassword'
#         )
#         other_comment = Comment.objects.create(
#             news=self.news,
#             author=other_user,
#             text='Other user comment'
#         )
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('news:edit', args=[other_comment.id]))
#         assert response.status_code == HTTPStatus.NOT_FOUND

#     def test_authorized_foreign_comment_delete(self):
#         other_user = User.objects.create_user(
#             username='anotheruser',
#             password='anotherpassword'
#         )
#         other_comment = Comment.objects.create(
#             news=self.news,
#             author=other_user,
#             text='Another user comment'
#         )
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('news:delete', args=[other_comment.id]))
#         assert response.status_code == HTTPStatus.NOT_FOUND
