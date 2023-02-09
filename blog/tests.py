from django.test import TestCase
from django.utils import timezone 
from django.contrib.auth.models import User
from .models import DeletedData, restore_post, Post
from rest_framework.test import APITestCase
from django.core.cache import cache
# Create your tests here.

class DeleteAndRestorePost(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', email='user@localhost')

    def test_delete_and_restore(self):
        post = Post(
            content='MyTestCase',
            date_posted= timezone.now(),
            author = self.user
        )
        post.save()
        model_id = post.id
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(DeletedData.objects.count(), 0)
        post.delete()
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(DeletedData.objects.count(), 1)
        restore_post(model_id)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(DeletedData.objects.count(), 0)

        print(timezone.now())

'''
class PostCreateViewTestCase(APITestCase):
    def test_create_is_throttled(self):
        self.user = User.objects.create(username='user', email='user@localhost')
        data = {'content': 'Lorem ipsium. Lorem ipsium. Lorem ipsium.', 'author': self.user}
        expected_num_objs = Post.objects.count() + 1

        self.assertFalse(cache.has_key('post_created'))
        response = self.client.post('/post/new/', data=data)
        self.assertTrue(cache.has_key('post_created'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), expected_num_objs)

        response = self.client.post('/post/new/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), expected_num_objs)'''