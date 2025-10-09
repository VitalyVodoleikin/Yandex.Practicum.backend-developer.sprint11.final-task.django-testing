from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture as lf


pytestmark = pytest.mark.django_db


class TestRoutes:

    @pytest.mark.parametrize(
        ['reverse_url', 'parametrized_client', 'status'],
        [
            (
                lf('home_url'),
                lf('another_user_client'),
                HTTPStatus.OK),
            (
                lf('detail_url'),
                lf('another_user_client'),
                HTTPStatus.OK),
            (
                lf('login_url'),
                lf('another_user_client'),
                HTTPStatus.OK),
            (
                lf('signup_url'),
                lf('another_user_client'),
                HTTPStatus.OK),

            (
                lf('edit_url'),
                lf('author_client'),
                HTTPStatus.OK),
            (
                lf('delete_url'),
                lf('author_client'),
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
            lf('logout_url'),
            lf('another_user_client'),
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
                lf('foreign_edit_url'),
                lf('author_client')),
            (
                lf('foreign_delete_url'),
                lf('author_client')),
            (
                lf('edit_url'),
                lf('another_user_client')),
            (
                lf('delete_url'),
                lf('another_user_client')),])
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
