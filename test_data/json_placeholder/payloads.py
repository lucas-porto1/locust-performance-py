import random

from faker import Faker

fake = Faker()


def generate_resource_id(minimum=1, maximum=50):
    return random.randint(minimum, maximum)


def create_post_payload():
    return {
        "title": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3),
        "userId": generate_resource_id(1, 10),
    }


def create_comment_payload():
    return {
        "name": fake.sentence(nb_words=5),
        "email": fake.email(),
        "body": fake.paragraph(nb_sentences=2),
        "postId": generate_resource_id(1, 100),
    }


def create_post_patch_payload():
    return {"title": fake.sentence(nb_words=6)}


def create_comment_patch_payload():
    return {"body": fake.sentence(nb_words=10)}
