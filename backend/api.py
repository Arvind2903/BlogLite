import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource
import backend.models as models
from flask_security import current_user, auth_required, logout_user
import hashlib
import os
import matplotlib.pyplot as plt
import numpy as np
import backend.tasks as tasks
from jinja2 import Template
from email_validator import validate_email, EmailNotValidError
from PIL import Image


mainDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
imgSaveDirectory = os.path.join(mainDirectory, 'frontend', "src", "assets", "images")
graphSaveDirectory = os.path.join(mainDirectory, 'frontend', "src", "assets", "graphs")
if not os.path.exists(imgSaveDirectory):
    os.makedirs(imgSaveDirectory)
if not os.path.exists(graphSaveDirectory):
    os.makedirs(graphSaveDirectory)

# For signup
class SignUpApi(Resource):

    #Invalid Requests
    def get(self):
        return "", "404 Invalid Request"

    def put(self):
        return "", "404 Invalid Request"

    def delete(self):
        return "", "404 Invalid Request"

    # Signing up User
    def post(self):
        username = request.json['username']
        email = request.json['email']
        try:
            v = validate_email(email)
            email = v["email"]
        except EmailNotValidError as e:
            return "", "406 {e}".format(e=str(e))
        name = request.json['name']
        phone = request.json['phone']
        bio = request.json['bio']
        password = request.json['password']

        username_val = models.User.query.filter_by(username=username).first()
        if username_val:
            return "", "405 Username Already Exists"
        email_val = models.User.query.filter_by(email=email).first()
        if email_val:
            return "", "404 Email Already Exists"

        user = models.User(username, email, name, phone, bio, password, active=True, fs_uniquifier = hashlib.md5(email.encode('utf-8')).hexdigest())
        models.db.session.add(user)
        models.db.session.commit()

        with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                               'WelcomeTemplate.html')) as file_:
            template = Template(file_.read())
            message = template.render(user=user)
        tasks.sendEmail(to_address=email, subject="Welcome to BlogLite",
                        message=message, attachments=[os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src',
                                                                 'assets', 'pdfs', 'Welcome.pdf')])

        return "", "200 Successfully Signed Up"


# For User
class UserApi(Resource):

    # Getting logged in user
    @auth_required('token')
    def get(self):
        activity = models.Activity(user_id=current_user.id, activity='login', timestamp=datetime.datetime.today())
        models.db.session.add(activity)
        models.db.session.commit()
        return models.user_schema.jsonify(current_user)

    # Getting user where user_id=id
    def post(self, id):
        user = models.User.query.filter_by(id=id).first()
        if user:
            user_json = models.user_schema.jsonify(user)
            activity = models.Activity(user_id=id, activity='visited profile', timestamp=datetime.datetime.today())
            models.db.session.add(activity)
            models.db.session.commit()
            return user_json
        else:
            return "", "404 User Not Found"

    # Editing user's profile details
    @auth_required('token')
    def put(self):
        user = models.User.query.filter_by(id=current_user.id).first()
        name = request.json['name']
        phone = request.json['phone']
        bio = request.json['bio']
        user.name = name
        user.phone = phone
        user.bio = bio
        models.db.session.commit()
        return models.user_schema.jsonify(user)

    # Deleting user's profile
    @auth_required('token')
    def delete(self):
        user = models.User.query.get(current_user.id)
        posts = models.Posts.query.filter_by(user_id=current_user.id).all()
        for post in posts:
            os.remove(os.path.join(imgSaveDirectory, str(post.id) + ".png"))
        csv_path = os.path.join(mainDirectory, "frontend", "src", "assets", "csvs", "{name}.csv".format(name=user.name))
        graph_path = os.path.join(mainDirectory, "frontend", "src", "assets", "csvs", "{name}.png".format(name=user.name))
        pdf_path = os.path.join(mainDirectory, "frontend", "src", "assets", "csvs", "{name}.pdf".format(name=user.name))
        for path in [csv_path, graph_path, pdf_path]:
            if os.path.exists(path):
                os.remove(path)
        models.db.session.delete(user)
        models.db.session.commit()
        return "", "200 Successfully Deleted Profile"



#For logging out
class LogoutApi(Resource):

    @auth_required('token')
    def get(self):
        logout_user()
        return "", "200 Successfully Logged Out User"

    # Invalid Requests
    def post(self):
        return "", "404 Invalid Request"

    def put(self):
        return "", "404 Invalid Request"

    def delete(self):
        return "", "404 Invalid Request"

from backend import cache
@cache.cached(key_prefix="getPosts()")
def getPosts():
    return models.Posts.query.all()

@cache.memoize()
def getPostsById(user_id):
    return models.Posts.query.filter_by(user_id=user_id).all()

# For homepage
class PostsApi(Resource):

    # Getting all Articles for HomePage
    def get(self):
        all_posts = getPosts()
        post_usernames = []
        for post in all_posts:
            post_usernames.append(post.author.username)
        results = models.posts_schema.dump(all_posts)
        for post in results:
            post['username'] = post_usernames[results.index(post)]
        usernames = [{"id":index+1,"username":user.username} for index,user in enumerate(models.User.query.all())]
        return make_response(jsonify({'posts':results, 'usernames':usernames}))

    # Getting all Articles of user with user_id=id
    def post(self, user_id):
        all_posts = getPostsById(user_id)
        results = models.posts_schema.dump(all_posts)
        return models.posts_schema.jsonify(results)

    # Invalid Requests
    def put(self):
        return "", "404 Invalid Request"

    def delete(self):
        return "", "404 Invalid Request"


# For posting content
class UserPostsApi(Resource):

    # Fetching Post with post_id=id
    @auth_required('token')
    def get(self, id):
        post = models.Posts.query.get(id)
        if post.author.id != current_user.id:
            activity = models.Activity(user_id=post.author.id, activity="visited post", timestamp=datetime.datetime.now())
            models.db.session.add(activity)
            models.db.session.commit()
        return models.post_schema.jsonify(post)

    # Adding Post
    @auth_required('token')
    def post(self):
        title = request.form.get('title')
        body = request.form.get('body')
        image = request.files['image']
        post = models.Posts(title, body, user_id=current_user.id, date=datetime.datetime.today(), img_url="")
        models.db.session.add(post)
        models.db.session.commit()
        image.save(os.path.join(imgSaveDirectory, str(post.id) + ".png"))
        post.img_url = os.path.join(imgSaveDirectory, str(post.id) + ".png")
        models.db.session.commit()
        cache.delete_memoized(getPostsById, post.author.id)
        return models.post_schema.jsonify(post)

    # Editing Post of id
    @auth_required('token')
    def put(self, id):
        post = models.Posts.query.get(id)
        title = request.form.get('title')
        body = request.form.get('body')
        if "image" in request.files:
            image = request.files['image']
            os.remove(os.path.join(imgSaveDirectory, str(id) + ".png"))
            image.save(os.path.join(imgSaveDirectory, str(id) + ".png"))
        post.title = title
        post.body = body
        models.db.session.commit()
        cache.delete_memoized(getPostsById, post.author.id)
        return models.post_schema.jsonify(post)

    # Deleting Post of id
    @auth_required('token')
    def delete(self, id):
        post = models.Posts.query.get(id)
        models.db.session.delete(post)
        models.db.session.commit()
        os.remove(os.path.join(imgSaveDirectory, str(id) + ".png"))
        cache.delete_memoized(getPostsById, post.author.id)
        return models.post_schema.jsonify(post)


# For Followings
class FollowingsApi(Resource):

    # Get followings
    def get(self, id):
        followings = models.Follow.query.filter_by(follower_id=id).all()
        followingsList = models.follows_schema.dump(followings)
        usernames = [following.is_following.username for following in followings]
        for following in followingsList:
            following['username'] = usernames[followingsList.index(following)]
        return jsonify(followingsList)

    # Add follower
    @auth_required('token')
    def post(self, id):
        follower = models.Follow(follower_id=current_user.id, following_id=id)
        activity = models.Activity(user_id=id, activity='followed', timestamp=datetime.datetime.today())
        models.db.session.add(follower)
        models.db.session.add(activity)
        models.db.session.commit()
        return "", "200 Successfully Added Follower"

    # Unfollow an account
    @auth_required('token')
    def delete(self, id):
        follower = models.Follow.query.filter_by(following_id=id).filter_by(follower_id=current_user.id).first()
        activity = models.Activity(user_id=id, activity='unfollowed', timestamp=datetime.datetime.today())
        models.db.session.delete(follower)
        models.db.session.add(activity)
        models.db.session.commit()
        return "", "200 Successfully Removed Follower"

    #Invalid Requests
    def put(self):
        return "", "404 Invalid Request"


# For Followers
class FollowersApi(Resource):

    # Get followers
    def get(self, id):
        followers = models.Follow.query.filter_by(following_id=id).all()
        followersList = models.follows_schema.dump(followers)
        usernames = [follower.is_follow.username for follower in followers]
        for follower in followersList:
            follower['username'] = usernames[followersList.index(follower)]
        return jsonify(followersList)

    # Check if following
    @auth_required('token')
    def post(self, id):
        follower =  models.Follow.query.filter_by(follower_id=current_user.id).filter_by(following_id=id).first()
        if follower:
            return make_response(jsonify({"isFollowing":True}))
        else:
            return make_response(jsonify({"isFollowing": False}))


# For Activity
class ActivityApi(Resource):

    # Get login, post, follow and unfollow activity
    @auth_required('token')
    def get(self):
        logins =  [login.timestamp for login in
                   models.Activity.query.filter_by(activity='login').filter_by(user_id=current_user.id).all()]
        follows = [follow.timestamp for follow in
                   models.Activity.query.filter_by(activity='followed').filter_by(user_id=current_user.id).all()]
        unfollows = [unfollow.timestamp for unfollow in
                     models.Activity.query.filter_by(activity='unfollowed').filter_by(user_id=current_user.id).all()]
        posts = [post.date for post in
                 models.Posts.query.filter_by(user_id=current_user.id).all()]
        activity = {'logins': logins,
                    'follows': follows,
                    'unfollows': unfollows,
                    'posts':posts}

        # If activity isn't there
        def emptyGraph(userActivityName, saveDirectory):
            plt.figure(figsize=(18, 8))
            numbers = [x for x in range(0, 24)]
            labels = map(lambda x: str(x), numbers)
            plt.xticks(numbers, labels)
            values = np.zeros(24)
            plt.xlim(1, 25)
            plt.plot(numbers, values)
            plt.yticks(range(0,1))
            plt.xlabel('Hour')
            plt.ylabel('{Values} in the last 24 hours'.format(Values=userActivityName))
            plt.tight_layout()
            plt.savefig(saveDirectory)
            plt.switch_backend('agg')

        # If activity is there
        def graph(userActivityName,userActivity, saveDirectory):
            plt.figure(figsize=(15, 10))
            hour_list = [t.hour for t in userActivity]
            numbers = [x for x in range(0, 24)]
            labels = map(lambda x: str(x), numbers)
            plt.xticks(numbers, labels)
            plt.xlim(1, 25)
            plt.yticks(range(1,hour_list.count(max(set(hour_list), key = hour_list.count))+1))
            values,bins,bars = plt.hist(hour_list, edgecolor='white', bins=list(range(1,25)))
            plt.margins(x=0.01, y=0.1)
            plt.bar_label(bars, fontsize=20, color='navy',
                          labels=[str(count) if count!=0 else "" for count in bars.datavalues])
            plt.xlabel('Hour')
            plt.ylabel('{Values} in 24 hours'.format(Values=userActivityName))
            plt.tight_layout()
            plt.savefig(saveDirectory)
            plt.switch_backend('agg')

        for key,value in activity.items():
            if not value:
                emptyGraph(key, os.path.join(graphSaveDirectory, "{name}.png".format(name=key)))
            else:
                graph(key, value, os.path.join(graphSaveDirectory, "{name}.png".format(name=key)))
        return "", "200 Successfully Made Graphs"



class JobApi(Resource):

    # export job to export csv and send as email
    @auth_required('token')
    def get(self):
        user_id = current_user.id
        r = tasks.generateCSV.delay(user_id)
        r.get()
        return "", "200 Successfully Queued Task"

    # import job to upload posts as csv
    @auth_required('token')
    def post(self):
        file = request.files['csv']
        csv = file.read().decode('latin-1')
        posts = csv.split('\r\n')
        for post in posts:
            try:
                title, body, url = post.split(',')
                post = models.Posts(title=title, body=body, user_id=current_user.id, date=datetime.datetime.now(),
                                    img_url="")
                models.db.session.add(post)
                models.db.session.commit()
                imgUrl = os.path.join(imgSaveDirectory, str(post.id) + ".png")
                img = Image.open(url)
                img.save(imgUrl)
                post.img_url = imgUrl
                cache.delete_memoized(getPostsById, post.author.id)
                models.db.session.commit()
            except FileNotFoundError:
                models.db.session.rollback()
                return "", "404 FileNotFoundError"
        return "", "200 Imported Posts Successfully"