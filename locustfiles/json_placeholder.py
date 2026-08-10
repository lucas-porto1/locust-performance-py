import os

from dotenv import load_dotenv
from locust import FastHttpUser, between, task

from clients.json_placeholder.comments_client import CommentsClient
from clients.json_placeholder.posts_client import PostsClient
from clients.json_placeholder.users_client import UsersClient
from test_data.json_placeholder.payloads import (
    create_comment_patch_payload,
    create_comment_payload,
    create_post_patch_payload,
    create_post_payload,
    generate_resource_id,
)

load_dotenv()


class JsonPlaceholderUser(FastHttpUser):
    host = os.environ["JSON_PLACEHOLDER_API_URL"]
    wait_time = between(2, 10)

    def on_start(self):
        self.posts_client = PostsClient(self.client)
        self.comments_client = CommentsClient(self.client)
        self.users_client = UsersClient(self.client)

    @task(3)
    def get_posts(self):
        self.posts_client.get_posts()

    @task(3)
    def get_comments(self):
        self.comments_client.get_comments()

    @task(2)
    def get_post(self):
        self.posts_client.get_post(generate_resource_id(1, 100))

    @task(2)
    def get_post_comments(self):
        self.posts_client.get_post_comments(generate_resource_id(1, 100))

    @task(2)
    def get_users(self):
        self.users_client.get_users()

    @task
    def get_user(self):
        self.users_client.get_user(generate_resource_id(1, 10))

    @task
    def get_user_todos(self):
        self.users_client.get_user_todos(generate_resource_id(1, 10))

    @task
    def create_post(self):
        self.posts_client.create_post(create_post_payload())

    @task
    def create_comment(self):
        self.comments_client.create_comment(create_comment_payload())

    @task
    def replace_post(self):
        self.posts_client.replace_post(generate_resource_id(), create_post_payload())

    @task
    def replace_comment(self):
        self.comments_client.replace_comment(
            generate_resource_id(), create_comment_payload()
        )

    @task
    def update_post(self):
        self.posts_client.update_post(
            generate_resource_id(), create_post_patch_payload()
        )

    @task
    def update_comment(self):
        self.comments_client.update_comment(
            generate_resource_id(), create_comment_patch_payload()
        )

    @task
    def delete_post(self):
        self.posts_client.delete_post(generate_resource_id())

    @task
    def delete_comment(self):
        self.comments_client.delete_comment(generate_resource_id())
