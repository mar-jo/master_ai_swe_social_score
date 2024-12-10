from SocialScores.Models.Post import PostBase, PostResponse
from datetime import datetime

table_name = "posts"

columns = {
    "id": "SERIAL PRIMARY KEY",
    '"user"': "TEXT NOT NULL",
    "text": "TEXT",
    "image": "TEXT",
    "time_created": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
}

class RepositoryPosts:
    def __init__(self, database):
        self.database = database

    def create_post(self, post: PostBase):
        self.database.insert(table_name, post.dict())

    def get_post_by_id(self, post_id: int):
        return self.database.fetchone(f"SELECT * FROM {table_name} WHERE id = %s", (post_id,))

    def get_latest_post(self):
        return self.database.fetchone(f"SELECT * FROM {table_name} ORDER BY time_created DESC LIMIT 1")

    def search_posts(self, query: str):
        return self.database.fetchall(f"SELECT * FROM {table_name} WHERE text LIKE %s", (f"%{query}%",))
