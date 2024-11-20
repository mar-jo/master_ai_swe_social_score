
class Post:
    def __init__(self, id, username, image, text):
        self.id = id
        self.username = username
        self.image = image
        self.text = text

    def __repr__(self):
        return f"<Post {self.id}>"