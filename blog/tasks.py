'''
from django.core.cache import cache
from .models import Comment, Post
from django.contrib.auth.models import User

#@app.task(bind=True)
def create_comment(self, user_id, text, post_id):
    cache_key = f"{user_id}/comment_created"
    if cache_key(cache_key):
        raise self.retry()
    obj = Comment.objects.create(content=text, author = User.objects.get(id=user_id), post_connected=Post.objects.get(id=post_id))
    obj.save
    cache.set(cache_key, obj.id, timeout=300)
    
'''