"""
Tests for /todos endpoint — JSONPlaceholder API
"""
import pytest
from schemas.post_schema import Todo


class TestGetTodos:

    def test_get_all_todos_returns_200(self, api_client, base_url):
        response = api_client.get(f"{base_url}/todos")
        assert response.status_code == 200

    def test_get_all_todos_returns_200_items(self, api_client, base_url):
        response = api_client.get(f"{base_url}/todos")
        assert len(response.json()) == 200

    def test_get_all_todos_schema_validation(self, api_client, base_url):
        response = api_client.get(f"{base_url}/todos")
        for item in response.json():
            todo = Todo(**item)
            assert isinstance(todo.completed, bool)
            assert len(todo.title) > 0

    def test_filter_completed_todos(self, api_client, base_url):
        response = api_client.get(f"{base_url}/todos", params={"completed": "true"})
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0
        for todo in todos:
            assert todo["completed"] is True

    def test_filter_incomplete_todos(self, api_client, base_url):
        response = api_client.get(f"{base_url}/todos", params={"completed": "false"})
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0
        for todo in todos:
            assert todo["completed"] is False

    def test_completed_and_incomplete_counts_add_up(self, api_client, base_url):
        total = len(api_client.get(f"{base_url}/todos").json())
        completed = len(api_client.get(f"{base_url}/todos", params={"completed": "true"}).json())
        incomplete = len(api_client.get(f"{base_url}/todos", params={"completed": "false"}).json())
        assert completed + incomplete == total

    @pytest.mark.parametrize("todo_id", [1, 50, 100, 200])
    def test_get_specific_todo_returns_200(self, api_client, base_url, todo_id):
        response = api_client.get(f"{base_url}/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["id"] == todo_id
