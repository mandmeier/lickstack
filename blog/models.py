from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=280, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(
        upload_to=upload_location, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    date_published = models.DateTimeField(
        auto_now=False, auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, auto_now_add=False, verbose_name="date updated")
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    #thumb = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/blog/article/{self.id}/'


@receiver(post_delete, sender=Article)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


# def pre_save_blog_post_receiver(sender, instance, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(
#             instance.author.username + "-" + instance.title)


# pre_save.connect(pre_save_blog_post_receiver, sender=Article)
