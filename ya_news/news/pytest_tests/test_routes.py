from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture

from django.contrib.auth import get_user_model


User = get_user_model()

pytestmark = pytest.mark.django_db


class TestRoutes:

    @pytest.mark.parametrize(
        ['reverse_url', 'parametrized_client', 'status'],
        [
            (
                lazy_fixture('home_url'),
                lazy_fixture('another_user_client'),
                HTTPStatus.OK),
            (
                lazy_fixture('detail_url'),
                lazy_fixture('another_user_client'),
                HTTPStatus.OK),
            (
                lazy_fixture('login_url'),
                lazy_fixture('another_user_client'),
                HTTPStatus.OK),
            (
                lazy_fixture('signup_url'),
                lazy_fixture('another_user_client'),
                HTTPStatus.OK),

            (
                lazy_fixture('edit_url'),
                lazy_fixture('author_client'),
                HTTPStatus.OK),
            (
                lazy_fixture('delete_url'),
                lazy_fixture('author_client'),
                HTTPStatus.OK),])
    def test_status_codes(
        self,
        reverse_url,
        parametrized_client,
        status
    ):
        response = parametrized_client.get(reverse_url)
        assert response.status_code == status

    @pytest.mark.parametrize(
        ['reverse_url', 'parametrized_client', 'status'],
        [(
            lazy_fixture('logout_url'),
            lazy_fixture('another_user_client'),
            HTTPStatus.OK
        )])
    def test_status_code_logout(
        self,
        reverse_url,
        parametrized_client,
        status
    ):
        response = parametrized_client.post(reverse_url)
        assert response.status_code == status

    @pytest.mark.parametrize(
        ['reverse_url', 'parametrized_client'],
        [
            (
                lazy_fixture('foreign_edit_url'),
                lazy_fixture('author_client')),
            (
                lazy_fixture('foreign_delete_url'),
                lazy_fixture('author_client')),
            (
                lazy_fixture('edit_url'),
                lazy_fixture('another_user_client')),
            (
                lazy_fixture('delete_url'),
                lazy_fixture('another_user_client')),])
    def test_redirects(
        self,
        reverse_url,
        parametrized_client,
        login_url
    ):
        response = parametrized_client.get(reverse_url)
        if response.status_code == HTTPStatus.NOT_FOUND:
            assert True
        else:
            assert response.status_code == HTTPStatus.FOUND
            assert response.url == f'{login_url}?next={reverse_url}'
