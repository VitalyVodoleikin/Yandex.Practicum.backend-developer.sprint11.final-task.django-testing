from http import HTTPStatus

import pytest

from news.forms import CommentForm
from django.conf import settings


pytestmark = pytest.mark.django_db


def test_news_count(client, home_url, news_list):
    """Тест проверки количества новостей на главной странице."""
    response = client.get(home_url)
    assert response.status_code == HTTPStatus.OK
    assert (
        response.context['object_list'].count()
        == settings.NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(client, home_url, news_list):
    """Тест проверки сортировки новостей."""
    response = client.get(home_url)
    all_news = response.context['object_list']
    dates = [news.date for news in all_news]
    assert dates == sorted(dates, reverse=True)


def test_comments_order(client, comments_list, detail_url):
    """Тест проверки сортировки комментариев."""
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK
    news = response.context['news']
    comments = news.comment_set.all()
    timestamps = [comment.created for comment in comments]
    sorted_timestamps = sorted(timestamps)
    assert timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, news, detail_url, db):
    """Тест проверки отсутствия формы комментария у анонимного пользователя."""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_user_has_form(author_client, news, detail_url):
    """Проверка наличия формы комментария у авторизованного пользователя."""
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
