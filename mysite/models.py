from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save
from tinymce import HTMLField
from django.dispatch import receiver


# Create your models here.
class PublishedModelManager(models.Manager):
    def get_queryset(self):
        return super(PublishedModelManager, self).get_queryset().filter(status='published')


class DraftModelManager(models.Manager):
    def get_queryset(self):
        return super(DraftModelManager, self).get_queryset().filter(status='draft')


class Post(models.Model):
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published')
    }

    title = models.CharField(max_length=100)
    content = HTMLField('content')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    object = models.Manager()
    draft = DraftModelManager()
    published = PublishedModelManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='post_images', blank=True, null=True)

    def __str__(self):
        return self.post.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Profile, self).save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_pro = (300, 300)
            img.thumbnail(output_pro)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class About(models.Model):
    about = models.TextField(max_length=2000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='replies')

    def __str__(self):
        return self.content
