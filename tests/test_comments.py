"""
Tests for /comments endpoint — JSONPlaceholder API
"""
from schemas.post_schema import Comment


class TestGetComments:

    def test_get_all_comments_returns_200(self, api_client, base_url):
        response = api_client.get(f"{base_url}/comments")
        assert response.status_code == 200

    def test_get_all_comments_returns_500_items(self, api_client, base_url):
        response = api_client.get(f"{base_url}/comments")
        assert len(response.json()) == 500

    def test_get_all_comments_schema_validation(self, api_client, base_url):
        response = api_client.get(f"{base_url}/comments")
        for item in response.json():
            comment = Comment(**item)
            assert comment.postId > 0
            assert "@" in comment.email

    def test_filter_comments_by_post_id(self, api_client, base_url):
        post_id = 1
        response = api_client.get(f"{base_url}/comments", params={"postId": post_id})
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) == 5
        for comment in comments:
            assert comment["postId"] == post_id

    def test_create_comment_returns_201(self, api_client, base_url, new_comment_payload):
        response = api_client.post(f"{base_url}/comments", json=new_comment_payload)
        assert response.status_code == 201

    def test_create_comment_returns_correct_data(self, api_client, base_url, new_comment_payload):
        response = api_client.post(f"{base_url}/comments", json=new_comment_payload)
        data = response.json()
        assert data["name"] == new_comment_payload["name"]
        assert data["email"] == new_comment_payload["email"]
        assert data["postId"] == new_comment_payload["postId"]

    def test_get_nonexistent_comment_returns_404(self, api_client, base_url):
        response = api_client.get(f"{base_url}/comments/99999")
        assert response.status_code == 404


class TestResponseHeaders:

    def test_content_type_is_json(self, api_client, base_url):
        response = api_client.get(f"{base_url}/comments/1")
        assert "application/json" in response.headers["Content-Type"]

    def test_response_time_under_threshold(self, api_client, base_url, response_threshold):
        response = api_client.get(f"{base_url}/comments")
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < response_threshold, (
            f"Response time {elapsed_ms:.0f}ms exceeded {response_threshold}ms"
        )
