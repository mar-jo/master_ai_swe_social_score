import Database as Database
import Models.Post as Post

def convert_post_to_dict(post: Post) -> dict:
    return {
        'id': post.id,
        'username': post.username,
        'image': post.image,
    }

table_name = 'posts'

columns = {
    'id': 'INTEGER',
    'username': 'TEXT',
    'image': 'BLOB',
}

class RepositoryPosts:
    def __init__(self, database: Database):
        self.database = database

    def add_post(self, post : Post):
        self.database.insert(table_name, convert_post_to_dict(post))

    def get_post(self, id):
        return self.database.fetchone(f"SELECT * FROM {table_name} WHERE id = ?", (id,))

    def get_all_posts(self):
        return self.database.fetchall(f"SELECT * FROM {table_name}")

    #def update_post(self, post):
    #    self.database.update_post(post)

    def delete_post(self, id):
        self.database.delete(table_name, "id = ?", (id,))