"""
Tests for /users endpoint — JSONPlaceholder API
"""
import pytest
from schemas.post_schema import User


class TestGetUsers:

    def test_get_all_users_returns_200(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users")
        assert response.status_code == 200

    def test_get_all_users_returns_10_items(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users")
        assert len(response.json()) == 10

    def test_get_all_users_schema_validation(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users")
        for user_data in response.json():
            user = User(**user_data)
            assert user.id > 0
            assert "@" in user.email

    def test_get_single_user_returns_200(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users/1")
        assert response.status_code == 200

    def test_get_user_posts(self, api_client, base_url):
        """A user should have associated posts."""
        response = api_client.get(f"{base_url}/users/1/posts")
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        for post in posts:
            assert post["userId"] == 1

    def test_get_user_todos(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users/1/todos")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_nonexistent_user_returns_404(self, api_client, base_url):
        response = api_client.get(f"{base_url}/users/99999")
        assert response.status_code == 404
