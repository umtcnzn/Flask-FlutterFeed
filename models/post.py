import uuid
from datetime import datetime
import humanize
from flask import session

class Post:
    def __init__(self, user_id, text, img="", likes=None, comments=None):
        self.post_id = str(uuid.uuid4())
        self.user_id = user_id
        self.text = text
        self.img = img if img else ""
        self.likes = likes if likes is not None else []
        self.comments = comments if comments is not None else []
        self.createdAt = datetime.now()

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "user_id" : self.user_id,
            "text" : self.text,
            "img" : self.img,
            "likes" : self.likes,
            "likeCount":len(self.likes),
            "comments" : self.comments,
            "commentCount":len(self.comments),
            "createdAt":self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "timeAgo" : humanize.naturaltime(datetime.now() - self.createdAt)
        }
    
    def to_post(self):
        return {
            "post_id": self.post_id,
            "text" : self.text,
            "img" : self.img,
            "likes" : self.likes,
            "likeCount":len(self.likes),
            "comments" : self.comments,
            "commentCount":len(self.comments),
            "createdAt":self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            "isLiked": session['user']['user_id'] in self.likes,
            "timeAgo" : humanize.naturaltime(datetime.now() - self.createdAt)
        }