class CommentsClient:
    def __init__(self, client):
        self.client = client

    def get_comments(self):
        with self.client.get("/comments", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get comments: {response.text}")

    def create_comment(self, payload):
        with self.client.post(
            "/comments", json=payload, catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Failed to create comment: {response.text}")

    def replace_comment(self, comment_id, payload):
        with self.client.put(
            f"/comments/{comment_id}",
            json=payload,
            name="/comments/{id}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Failed to replace comment {comment_id}: {response.text}"
                )

    def update_comment(self, comment_id, payload):
        with self.client.patch(
            f"/comments/{comment_id}",
            json=payload,
            name="/comments/{id}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Failed to update comment {comment_id}: {response.text}"
                )

    def delete_comment(self, comment_id):
        with self.client.delete(
            f"/comments/{comment_id}",
            name="/comments/{id}",
            catch_response=True,
        ) as response:
            if response.status_code not in (200, 204):
                response.failure(
                    f"Failed to delete comment {comment_id}: {response.text}"
                )
