import datetime
from time import timezone

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from .const import COUNT_OF_COMMENTS


@pytest.fixture
def author(django_user_model):
    """Создание автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def another_user(django_user_model):
    """Создаёт стороннего пользоваетля."""
    return django_user_model.objects.create(username='Сторонний пользователь')


@pytest.fixture
def author_client(author):
    """Авторизация автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_user_client(another_user):
    """Авторизация стороннего пользователя."""
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def news(db):
    """Создание новости."""
    return News.objects.create(
        title='Заголовок',
        text='Текст')


@pytest.fixture
def comment(news, author):
    """Создание комментария."""
    comment = Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author,)
    return comment


@pytest.fixture
def news_list(db):
    """Создание списка новостей."""
    today = datetime.date.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        News.objects.create(
            title=f'Еще одна свежая новость {index}',
            text='Текст еще одной свежей новости.',
            date=today - datetime.timedelta(days=index))


@pytest.fixture
def comments_list(author, news):
    """Создание списка комментариев."""
    now = timezone.now()
    for index in range(COUNT_OF_COMMENTS):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',)
        comment.created = now + datetime.timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    """URL главной страницы."""
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    """URL страницы новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    """URL редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    """URL удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def login_url():
    """URL страницы входа."""
    return reverse('users:login')


@pytest.fixture
def signup_url():
    """URL страницы регистрации."""
    return reverse('users:signup')


@pytest.fixture
def logout_url():
    """URL страницы выхода."""
    return reverse('users:logout')









# # ==========
# import datetime
# from time import timezone

# import pytest
# from django.conf import settings
# from django.test import Client
# from django.urls import reverse
# from django.utils import timezone

# from news.models import Comment, News
# from .const import COUNT_OF_COMMENTS


# @pytest.fixture
# def author(django_user_model):
#     """Создание автора."""
#     return django_user_model.objects.create(username='Автор')


# @pytest.fixture
# def another_user(django_user_model):
#     """Создаёт стороннего пользоваетля."""
#     return django_user_model.objects.create(username='Сторонний пользователь')


# @pytest.fixture
# def author_client(author):
#     """Авторизация автора."""
#     client = Client()
#     client.force_login(author)
#     return client


# @pytest.fixture
# def another_user_client(another_user):
#     """Авторизация стороннего пользователя."""
#     client = Client()
#     client.force_login(another_user)
#     return client


# @pytest.fixture
# def news(db):
#     """Создание новости."""
#     return News.objects.create(
#         title='Заголовок',
#         text='Текст')


# @pytest.fixture
# def comment(news, author):
#     """Создание комментария."""
#     comment = Comment.objects.create(
#         news=news,
#         text='Текст комментария',
#         author=author,)
#     return comment


# @pytest.fixture
# def news_list(db):
#     """Создание списка новостей."""
#     today = datetime.date.today()
#     for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
#         News.objects.create(
#             title=f'Еще одна свежая новость {index}',
#             text='Текст еще одной свежей новости.',
#             date=today - datetime.timedelta(days=index))


# @pytest.fixture
# def comments_list(author, news):
#     """Создание списка комментариев."""
#     now = timezone.now()
#     for index in range(COUNT_OF_COMMENTS):
#         comment = Comment.objects.create(
#             news=news, author=author, text=f'Tекст {index}',)
#         comment.created = now + datetime.timedelta(days=index)
#         comment.save()


# @pytest.fixture
# def home_url():
#     """URL главной страницы."""
#     return reverse('news:home')


# @pytest.fixture
# def detail_url(news):
#     """URL страницы новости."""
#     return reverse('news:detail', args=(news.id,))


# @pytest.fixture
# def edit_url(comment):
#     """URL редактирования комментария."""
#     return reverse('news:edit', args=(comment.id,))


# @pytest.fixture
# def delete_url(comment):
#     """URL удаления комментария."""
#     return reverse('news:delete', args=(comment.id,))


# @pytest.fixture
# def login_url():
#     """URL страницы входа."""
#     return reverse('users:login')


# @pytest.fixture
# def signup_url():
#     """URL страницы регистрации."""
#     return reverse('users:signup')
