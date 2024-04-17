from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_security import SQLAlchemyUserDatastore, UserMixin
from backend.database import db


ma = Marshmallow()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.Integer(), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), nullable=False, unique=True) # Used to generate auth token
    posts = db.relationship('Posts', cascade='all, delete-orphan', back_populates='author')
    followers = db.relationship('Follow', cascade='all, delete-orphan', back_populates='is_follow', foreign_keys="Follow.follower_id")
    followings = db.relationship('Follow', cascade='all, delete-orphan', back_populates='is_following', foreign_keys="Follow.following_id")
    activity = db.relationship('Activity', cascade='all, delete-orphan', back_populates='active_user')

    def __init__(self, username, email, name, phone, bio, password, active, fs_uniquifier):
        self.username = username
        self.email = email
        self.name = name
        self.phone = phone
        self.bio = bio
        self.active = active
        self.fs_uniquifier = fs_uniquifier
        self.password = password


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    author = db.relationship('User', back_populates='posts', lazy="subquery")

    def __init__(self, title, body, user_id, date, img_url):
        self.title = title
        self.body = body
        self.date = date
        self.user_id = user_id
        self.img_url = img_url


class Follow(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_follow = db.relationship('User', back_populates='followers', foreign_keys="Follow.follower_id")
    is_following = db.relationship('User', back_populates='followings', foreign_keys="Follow.following_id")

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime())
    active_user = db.relationship('User', back_populates='activity')

    def __init__(self, activity, timestamp, user_id):
        self.activity = activity
        self.timestamp = timestamp
        self.user_id = user_id



class FollowSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    follower_id = fields.Int()
    following_id = fields.Int()

    class Meta:
        include_fk = True
        include_relationships = True


class PostSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    body = fields.Str()
    date = fields.Str()
    user_id = fields.Int()
    img_url = fields.Str()

    class Meta:
        include_fk = True
        include_relationships = True


class ActivitySchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    activity = fields.Str()
    user_id = fields.Int()
    timestamp = fields.Str()

    class Meta:
        include_fk = True
        include_relationships = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    name = fields.Str()
    phone = fields.Int()
    bio = fields.Str()
    posts = fields.Nested(PostSchema, many=True)
    followers = fields.Nested(FollowSchema, many=True)
    following = fields.Nested(FollowSchema, many=True)
    activity = fields.Nested(ActivitySchema, many=True)

    class Meta:
        include_relationships = True


follows_schema = FollowSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()

user_datastore = SQLAlchemyUserDatastore(db, User, None)
