class User:
    def __init__(self, _id, username, discriminator, avatar):
        self.id = _id
        self.username = username
        self.discriminator = discriminator
        self.avatar = avatar
        self.tag = username + "#" + discriminator