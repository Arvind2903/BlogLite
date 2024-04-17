import datetime
from backend.workers import celery
from celery.schedules import crontab
import backend.models as models
from flask import current_app as app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import matplotlib.pyplot as plt
from jinja2 import Template
from weasyprint import HTML
import pandas as pd

host = app.config['SMTP_SERVER_HOST']
port = app.config['SMTP_SERVER_PORT']
sender_address = app.config['SENDER_ADDRESS']
sender_password = app.config['SENDER_PASSWORD']
mainDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
graphSaveDirectory = os.path.join(mainDirectory, 'frontend', "src", "assets", "graphs")
THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep
base_url = 'file://' + THIS_FILE_DIR

# Function to check if the user has logged in that day
def loginCheck(user):
    today_day = datetime.datetime.now().day
    logins = models.Activity.query.filter_by(user_id=user.id).filter_by(activity='login').all()
    for activity in logins:
        if activity.timestamp.day == today_day:
            return True
    return False

# Function to check if the user has posted that day
def postCheck(user):
    today_day = datetime.datetime.now().day
    posts = models.Posts.query.filter_by(user_id=user.id).all()
    for activity in posts:
        if activity.date.day == today_day:
            return True
    return False

# General function to email MailHog
def sendEmail(to_address, subject, message, attachments=None):
    msg = MIMEMultipart()
    msg["From"] = sender_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachments:
        for attachment in attachments:
            if attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attachment, "rb").read())
                part.add_header(
                    "Content-Disposition", f"attachment; filename= {os.path.basename(attachment)}"
                )
                encode_base64(part)
                msg.attach(part)

    s = smtplib.SMTP(host=host, port=port)
    s.login(sender_address, sender_password)
    s.send_message(msg)
    s.quit()


# Send reminder if not logged/posted
@celery.task()
def sendReminders():
    users = models.User.query.all()
    recipients = []
    for user in users:
        if not loginCheck(user):
            with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                                   'LoginReminderTemplate.html')) as file_:
                template = Template(file_.read())
                message = template.render(user=user)
            recipients.append({"name": user.name, "email": user.email, "subject": "Login Reminder",
                               "message": message})
        elif loginCheck(user) and not postCheck(user):
            with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                                   'PostReminderTemplate.html')) as file_:
                template = Template(file_.read())
                message = template.render(user=user)
            recipients.append({"name": user.name, "email": user.email, "subject": "Post Reminder",
                               "message": message})

    for user in recipients:
        sendEmail(to_address=user["email"], subject=user["subject"], message=user["message"])


# Send monthly reports
@celery.task()
def sendReports():
    users = models.User.query.all()
    now = datetime.datetime.now() - datetime.timedelta(days=1)
    month = now.strftime("%B")
    oneMonthBack = now - datetime.timedelta(days=10)
    twoMonthsBack =  now - datetime.timedelta(days=20)
    activities = ["login", "visited profile", "visited post", "followed", "unfollowed"]
    for user in users:
        bar1, bar2 = [], []
        for activity in activities:
            oneMonth = len([item.timestamp for item in models.db.session.query(models.Activity).filter_by(user_id=user.id).
                        filter_by(activity=activity).filter(models.Activity.timestamp>oneMonthBack).all()])
            twoMonths = len([item.timestamp for item in models.db.session.query(models.Activity).filter_by(user_id=user.id).
                        filter_by(activity=activity).filter(models.Activity.timestamp > twoMonthsBack).
                        filter(models.Activity.timestamp<=oneMonthBack).all()])
            if activity=="login":
                current_month_logins = oneMonth
                previous_month_logins = twoMonths
            bar1.append(oneMonth)
            bar2.append(twoMonths)
        data = {'Last Month':bar1, 'Month Before':bar2}
        df = pd.DataFrame(data, index=activities)
        plt.figure(figsize=(4, 6))
        ax = df.plot(kind='bar', rot=0, xlabel="Activity", ylabel="",
                     title='Engagement Graph for {user}'.format(user=user.name))
        for c in ax.containers:
            ax.bar_label(c, label_type='edge',
                         labels=[str(count) if count!=0 else "" for count in c.datavalues])
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(os.path.join(graphSaveDirectory, "{user}.png".format(user=user.name)))
        plt.switch_backend('agg')
        with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                               'ReportTemplate.html')) as file_:
            template = Template(file_.read())
            message = template.render(user=user, current_month_logins=current_month_logins,
                                      previous_month_logins=previous_month_logins, month=month)
            html = HTML(string=message, base_url=base_url)
            file_name = os.path.join(mainDirectory, 'frontend', 'src', 'assets', 'pdfs', "{name}.pdf".format(name=user.name))
            html.write_pdf(target=file_name)
        with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                               'ReportMessageTemplate.html')) as file_:
            template = Template(file_.read())
            message = template.render(user=user, month=month)
            sendEmail(to_address=user.email, subject="Monthly Engagement Report",
                  message=message, attachments=[os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src','assets',
                                                           'pdfs', '{name}.pdf'.format(name=user.name))])



# User triggered async export job
@celery.task()
def generateCSV(user_id):
    user = models.User.query.get(user_id)
    posts = models.Posts.query.filter_by(user_id=user_id).all()
    nPosts = len(posts)
    nFollowers = len(models.Follow.query.filter_by(following_id=user_id).all())
    nFollowings = len(models.Follow.query.filter_by(follower_id=user_id).all())
    user_data = {
        "Username": user.name,
        "Email": user.email,
        "Full Name": user.name,
        "Number of Posts": nPosts,
        "Number of Followers": nFollowers,
        "Number of Followings": nFollowings
    }
    post_data = {
        "Post Title": [post.title for post in posts],
        "Post Body": [post.body for post in posts],
        "Post Timestamp": [post.date for post in posts],
        "Post Image": [post.img_url for post in posts]
    }
    df_user = pd.DataFrame([user_data])
    df_posts = pd.DataFrame(post_data)
    file_name_user = os.path.join(mainDirectory, 'frontend', 'src', 'assets', 'csvs', "{name}.csv".format(name=user.name))
    file_name_post = os.path.join(mainDirectory, 'frontend', 'src', 'assets', 'csvs',
                                  "{name}_posts.csv".format(name=user.name))
    df_user.to_csv(file_name_user, index=False)
    df_posts.to_csv(file_name_post, index=False)
    with open(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'templates',
                           'CSVMessageTemplate.html')) as file_:
        template = Template(file_.read())
        message = template.render(user=user)
    sendEmail(to_address=user.email, subject="User Dashboard",
              message=message, attachments=[os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'assets',
                                                       'csvs', '{name}.csv'.format(name=user.name)),
                                            os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'assets',
                                                         'csvs', '{name}_posts.csv'.format(name=user.name))
                                            ])


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    # Every morning at 10 AM
    sender.add_periodic_task(crontab(hour=10, minute=0),
                             sendReminders.s(),
                             name="daily reminders")

    # Every month beginning
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0),
                             sendReports.s(),
                             name="monthly reports")
