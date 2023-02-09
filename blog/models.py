from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from rest_framework import serializers
from django.core import serializers

bad_words = ['fuck', 'pussy', 'nigga', 'ass']

def validate_no_bad_word(content):
    if any([word in content.lower() for word in bad_words]):
        raise ValidationError("No bad words allowed!")



class Post(models.Model):
    content = models.TextField(max_length=1000, validators=[validate_no_bad_word])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def __str__(self):
        return self.content[:5]

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()


class Comment(models.Model):
    content = models.TextField(max_length=150, validators=[validate_no_bad_word])
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)


class Preference(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")


class ActivityLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.user}, {self.action}'

    @receiver(post_save, sender=Post)
    def _post_save_activity_log(sender, instance, **kwargs):
        user = User.objects.get(email = instance.author.email)
        ActivityLog.objects.create(
            user = user,
            action = f'User #{user.id} {user.email} saved post {instance.id}'
        )
        

class DeletedData(models.Model):
    model_type = models.CharField(max_length=200)
    model_id = models.IntegerField()
    data = models.TextField()

    @receiver(post_delete, sender=Post)
    def archive_posts(sender, instance, **kwargs):
        data = serializers.serialize('json', [instance])
        DeletedData.objects.create(
            model_type = 'Post',
            model_id = instance.id,
            data = data
        )

def restore_post(id):
    deleted = DeletedData.objects.get(
        model_type = 'Post',
        model_id = id,
    )
    for instance in serializers.deserialize('json', deleted.data):
        instance.save()
        deleted.delete()


    