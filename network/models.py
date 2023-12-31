from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name = "followers", symmetrical=False)
    
    def to_dict(self, request):
        follow = False
        if self.followers.filter(id = request.user.id).exists():
            follow = True
        else:
            follow = False
        return{
            'id': self.id,
            'username':self.username,
            'followers': self.followers.count(),
            'following': self.following.count(),
            'follow': follow,
            'posts': self.posts.count(),
        }

class Post(models.Model):
    title = models.CharField(max_length = 250, blank = False)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "posts")
    post =  models.CharField(max_length = 250, blank = False)
    date = models.DateTimeField(auto_now_add = True)
    like = models.ManyToManyField(User, related_name= "likes")
    
    def __str__(self):
        return f"{self.title}, {self.user.username}"
    
    def to_dict(self, request):
        liked = False
        if self.like.filter(id = request.user.id).exists():
            liked = True
        return{
            'id': self.id,
            'user': self.user.username,
            'title': self.title,
            'date': self.date.strftime("%B %d, %Y, %I:%M %p"),
            'post': self.post,
            'like': self.like.count(),
            'liked': liked,
        }
 
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comments")
    date = models.DateTimeField(auto_now_add = True)
    comment = models.CharField(max_length = 250, blank = False)
    like = models.ManyToManyField(User, related_name = "Clike")
    
    def __str__(self):
        return f"{self.post.title}, {self.user.username}"
    
    