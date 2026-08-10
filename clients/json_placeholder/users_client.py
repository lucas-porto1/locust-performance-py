class UsersClient:
    def __init__(self, client):
        self.client = client

    def get_users(self):
        with self.client.get("/users", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get users: {response.text}")

    def get_user(self, user_id):
        with self.client.get(
            f"/users/{user_id}", name="/users/{id}", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get user {user_id}: {response.text}")

    def get_user_todos(self, user_id):
        with self.client.get(
            f"/users/{user_id}/todos",
            name="/users/{id}/todos",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Failed to get todos for user {user_id}: {response.text}"
                )
