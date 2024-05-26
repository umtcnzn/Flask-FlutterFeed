import uuid
from datetime import datetime
class User:

    def __init__(self,name,username,email,password,profilePic = "avatar.png",followers= None, following = None,bio = ""):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.profilePic = profilePic if profilePic else ""
        self.followers = followers if followers is not None else []
        self.following = following if following is not None else []
        self.bio = bio if bio else ""
        self.createdAt = datetime.now()

    def to_dict(self):
        return{
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "name" : self.name,
            "profilePic" : self.profilePic,
            "bio" : self.bio,
            "followers" : self.followers,
            "following" : self.following,
            "followersCount": len(self.followers),
            "followingCount": len(self.following),
            "createdAt" : self.createdAt
        }
    
    def to_post(self):
        return{
            "username": self.username,
            "name" : self.name,
            "profilePic" : self.profilePic,
            "followersCount": len(self.followers),
            "followingCount": len(self.following),
        }

    