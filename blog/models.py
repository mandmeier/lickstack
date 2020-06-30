from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_delete
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from markdown_deux import markdown
from comments.models import Comment
from repo.models import Lick
from taggit.managers import TaggableManager


class ArticleManager(models.Manager):
    # create Article.objects.active() method
    def active(self, *args, **kwargs):
        return super(ArticleManager, self).filter(draft=False).filter(date_published__lte=timezone.now())


def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Category(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter a blog post category', blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=280, null=False, blank=False)
    body = models.TextField(max_length=50000, null=False, blank=False)
    image = models.ImageField(
        upload_to=upload_location, blank=True, width_field="width_field", height_field="height_field")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, default='', null=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    date_published = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="date published")
    date_created = models.DateTimeField(
        auto_now=False, auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(
        auto_now=True, auto_now_add=False, verbose_name="date updated")
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    #thumb = models.ImageField(default='default.png', blank=True)
    licks = models.ManyToManyField(Lick, blank=True)
    lick_string = models.CharField(max_length=50, null=True, blank=True)
    transpose_string = models.CharField(max_length=50, null=True, blank=True)
    lick_placeholders_string = models.CharField(
        max_length=200, null=True, blank=True)
    tags = TaggableManager()

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article-detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        content = self.body
        return mark_safe(markdown(content))

    def save(self, *args, **kwargs):
        if not self.lick_string == None:
            ids = [int(id) for id in self.lick_string.split(',')]
            licks = Lick.objects.filter(id__in=ids).distinct()
            super().save(*args, **kwargs)
            self.licks.add(*licks)  # add licks to many to many field
        super().save(*args, **kwargs)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(
            instance.__class__).model
        return content_type

# deletes images from AWS if post is deleted


@receiver(post_delete, sender=Article)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_blog_post_receiver, sender=Article)
