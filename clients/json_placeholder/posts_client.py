class PostsClient:
    def __init__(self, client):
        self.client = client

    def get_posts(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get posts: {response.text}")

    def get_post(self, post_id):
        with self.client.get(
            f"/posts/{post_id}", name="/posts/{id}", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get post {post_id}: {response.text}")

    def get_post_comments(self, post_id):
        with self.client.get(
            f"/posts/{post_id}/comments",
            name="/posts/{id}/comments",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Failed to get comments for post {post_id}: {response.text}"
                )

    def create_post(self, payload):
        with self.client.post("/posts", json=payload, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Failed to create post: {response.text}")

    def replace_post(self, post_id, payload):
        with self.client.put(
            f"/posts/{post_id}",
            json=payload,
            name="/posts/{id}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to replace post {post_id}: {response.text}")

    def update_post(self, post_id, payload):
        with self.client.patch(
            f"/posts/{post_id}",
            json=payload,
            name="/posts/{id}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to update post {post_id}: {response.text}")

    def delete_post(self, post_id):
        with self.client.delete(
            f"/posts/{post_id}", name="/posts/{id}", catch_response=True
        ) as response:
            if response.status_code not in (200, 204):
                response.failure(f"Failed to delete post {post_id}: {response.text}")
