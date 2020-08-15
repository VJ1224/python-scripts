import praw
import os
import sys
import smtplib
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(client_id=os.getenv('REDDIT_ID'), 
                    client_secret=os.getenv('REDDIT_SECRET'),
                    password=os.getenv('REDDIT_PASSWORD'),
                    user_agent='PrawTut',
                    username=os.getenv('REDDIT_USERNAME'))


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <subreddit>")
        return

    print("Logged in")

    subreddit_name = sys.argv[1]
    subreddit = reddit.subreddit(subreddit_name)
    new_posts = subreddit.new(limit=5)

    print("Posts retrieved")

    content = ""

    for post in new_posts:
        content = content + post.title + "\n"
        content = content + post.url + "\n\n"

    email = os.getenv('GMAIL_EMAIL')
    message = "\r\n".join([
        "From: " + email,
        "To: " + email,
        "Subject: New posts on " + subreddit_name,
        "",
        content
        ])

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(email, os.getenv('GMAIL_PASSWORD'))

    session.sendmail(email, email, message.encode('utf-8'))
    session.quit()

    print("Mail sent")

if __name__ == "__main__":
    main()