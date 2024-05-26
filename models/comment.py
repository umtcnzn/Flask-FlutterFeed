import uuid
from datetime import datetime
import humanize
from flask import session

class Comment:

    def __init__(self,user_id,post_id,text,likes = None):
        self.comment_id = str(uuid.uuid4())
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.likes = likes if likes is not None else []
        self.createdAt = datetime.now()


    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
            "likes": self.likes,
            "likeCount": len(self.likes),
            "createdAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def to_post(self):
        return{
            "comment_id": self.comment_id,
            "post_id": self.post_id,
            "text": self.text,
            "likes": self.likes,
            "likeCount": len(self.likes),
            "timeAgo" : humanize.naturaltime(datetime.now() - self.createdAt),
            "isLiked": session['user']['user_id'] in self.likes,
            "createdAt": self.createdAt.strftime("%Y-%m-%d %H:%M:%S")
        }
        