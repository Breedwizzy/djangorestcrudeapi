from pickle import TRUE
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()


def upload_to(instance, filename):
    return 'Posts/{filename}'.format(filename=filename)


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(_('image'),
                              upload_to='media/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Posts')
    likes = models.ManyToManyField(
        User, blank=True, related_name='liked_posts')
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


'''
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    '''
