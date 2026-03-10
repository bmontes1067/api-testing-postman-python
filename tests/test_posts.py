"""
Tests for /posts endpoint — JSONPlaceholder API
Covers: GET list, GET single, POST, PUT, PATCH, DELETE
+ schema validation, response time, negative cases
"""
import pytest
import requests
from schemas.post_schema import Post, PostCreate


class TestGetPosts:

    def test_get_all_posts_returns_200(self, api_client, base_url, response_threshold):
        response = api_client.get(f"{base_url}/posts")
        assert response.status_code == 200

    def test_get_all_posts_returns_100_items(self, api_client, base_url):
        response = api_client.get(f"{base_url}/posts")
        data = response.json()
        assert len(data) == 100

    def test_get_all_posts_response_time(self, api_client, base_url, response_threshold):
        response = api_client.get(f"{base_url}/posts")
        assert response.elapsed.total_seconds() * 1000 < response_threshold, (
            f"Response time {response.elapsed.total_seconds() * 1000:.0f}ms "
            f"exceeded threshold of {response_threshold}ms"
        )

    def test_get_all_posts_schema_validation(self, api_client, base_url):
        response = api_client.get(f"{base_url}/posts")
        posts = response.json()
        for post in posts:
            validated = Post(**post)
            assert validated.id > 0
            assert validated.userId > 0
            assert len(validated.title) > 0

    def test_get_single_post_returns_200(self, api_client, base_url, existing_post_id):
        response = api_client.get(f"{base_url}/posts/{existing_post_id}")
        assert response.status_code == 200

    def test_get_single_post_returns_correct_id(self, api_client, base_url, existing_post_id):
        response = api_client.get(f"{base_url}/posts/{existing_post_id}")
        data = response.json()
        assert data["id"] == existing_post_id

    def test_get_single_post_schema_validation(self, api_client, base_url, existing_post_id):
        response = api_client.get(f"{base_url}/posts/{existing_post_id}")
        post = Post(**response.json())
        assert post.id == existing_post_id
        assert isinstance(post.title, str)
        assert isinstance(post.body, str)

    def test_get_post_comments(self, api_client, base_url, existing_post_id):
        response = api_client.get(f"{base_url}/posts/{existing_post_id}/comments")
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        for comment in comments:
            assert comment["postId"] == existing_post_id

    def test_filter_posts_by_user_id(self, api_client, base_url):
        user_id = 1
        response = api_client.get(f"{base_url}/posts", params={"userId": user_id})
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        for post in posts:
            assert post["userId"] == user_id


class TestCreatePost:

    def test_create_post_returns_201(self, api_client, base_url, new_post_payload):
        response = api_client.post(f"{base_url}/posts", json=new_post_payload)
        assert response.status_code == 201

    def test_create_post_returns_correct_data(self, api_client, base_url, new_post_payload):
        response = api_client.post(f"{base_url}/posts", json=new_post_payload)
        data = response.json()
        assert data["title"] == new_post_payload["title"]
        assert data["body"] == new_post_payload["body"]
        assert data["userId"] == new_post_payload["userId"]

    def test_create_post_returns_new_id(self, api_client, base_url, new_post_payload):
        response = api_client.post(f"{base_url}/posts", json=new_post_payload)
        data = response.json()
        assert "id" in data
        assert data["id"] == 101  # JSONPlaceholder always returns 101

    def test_create_post_schema_validation(self, api_client, base_url, new_post_payload):
        response = api_client.post(f"{base_url}/posts", json=new_post_payload)
        post = PostCreate(**response.json())
        assert post.title == new_post_payload["title"]


class TestUpdatePost:

    def test_put_post_returns_200(self, api_client, base_url, existing_post_id, new_post_payload):
        response = api_client.put(
            f"{base_url}/posts/{existing_post_id}",
            json={**new_post_payload, "id": existing_post_id}
        )
        assert response.status_code == 200

    def test_put_post_updates_all_fields(self, api_client, base_url, existing_post_id, new_post_payload):
        payload = {**new_post_payload, "id": existing_post_id, "title": "Updated Title"}
        response = api_client.put(f"{base_url}/posts/{existing_post_id}", json=payload)
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["id"] == existing_post_id

    def test_patch_post_returns_200(self, api_client, base_url, existing_post_id):
        response = api_client.patch(
            f"{base_url}/posts/{existing_post_id}",
            json={"title": "Patched Title"}
        )
        assert response.status_code == 200

    def test_patch_post_updates_only_title(self, api_client, base_url, existing_post_id):
        response = api_client.patch(
            f"{base_url}/posts/{existing_post_id}",
            json={"title": "Only Title Changed"}
        )
        data = response.json()
        assert data["title"] == "Only Title Changed"
        assert data["id"] == existing_post_id


class TestDeletePost:

    def test_delete_post_returns_200(self, api_client, base_url, existing_post_id):
        response = api_client.delete(f"{base_url}/posts/{existing_post_id}")
        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api_client, base_url, existing_post_id):
        response = api_client.delete(f"{base_url}/posts/{existing_post_id}")
        assert response.json() == {}


class TestNegativeCases:

    def test_get_nonexistent_post_returns_404(self, api_client, base_url):
        response = api_client.get(f"{base_url}/posts/99999")
        assert response.status_code == 404

    def test_get_nonexistent_post_returns_empty_body(self, api_client, base_url):
        response = api_client.get(f"{base_url}/posts/99999")
        assert response.json() == {}

    @pytest.mark.parametrize("invalid_id", ["abc", "!@#", "0", "-1"])
    def test_get_post_with_invalid_id(self, api_client, base_url, invalid_id):
        response = api_client.get(f"{base_url}/posts/{invalid_id}")
        assert response.status_code in [400, 404]
