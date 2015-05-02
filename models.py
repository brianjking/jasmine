import peewee as p

db = p.SqliteDatabase('jasmine.db')

# Common model definition
class BaseModel(p.Model):
    class Meta:
        database = db

# Core objects
class User(BaseModel):
    identifier = p.CharField(unique=True)
    name = p.CharField(unique=True)
    avatar = p.TextField()
    raw = p.TextField()

    @property
    def channels(self):
        return Channel.select().join(UserChannel).where(UserChannel.user == self)


class Channel(BaseModel):
    identifier = p.CharField(unique=True)
    name = p.CharField(unique=True)
    raw = p.TextField()

    @property
    def users(self):
        return User.select().join(UserChannel).where(UserChannel.channel == self)

    @property
    def messages(self):
        return Message.select().join(ChannelMessage).where(ChannelMessage.channel == self)


class Group(BaseModel):
    identifier = p.CharField(unique=True)
    name = p.CharField(unique=True)
    raw = p.TextField()

    @property
    def users(self):
        return User.select().join(UserGroup).where(UserGroup.group == self)

    @property
    def messages(self):
        return Message.select().join(GroupMessage).where(GroupMessage.channel == self)


class Im(BaseModel):
    identifier = p.CharField(unique=True)
    user = p.ForeignKeyField(User, unique=True)
    raw = p.TextField()

    @property
    def messages(self):
        return Message.select().join(ImMessage).where(ImMessage.channel == self)


class Message(BaseModel):
    type = p.CharField()
    user = p.ForeignKeyField(User)
    text = p.TextField(null=True)
    timestamp = p.DateTimeField()
    raw = p.TextField()


# Relations
class UserChannel(BaseModel):
    user = p.ForeignKeyField(User)
    channel = p.ForeignKeyField(Channel)

class UserGroup(BaseModel):
    user = p.ForeignKeyField(User)
    group = p.ForeignKeyField(Group)

class ChannelMessage(BaseModel):
    channel = p.ForeignKeyField(Channel)
    message = p.ForeignKeyField(Message, unique=True)

class GroupMessage(BaseModel):
    group = p.ForeignKeyField(Group)
    message = p.ForeignKeyField(Message, unique=True)

class ImMessage(BaseModel):
    im = p.ForeignKeyField(Im)
    message = p.ForeignKeyField(Message, unique=True)
