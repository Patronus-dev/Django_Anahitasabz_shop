from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Blog(models.Model):
    STATUS_CHOICES = (
        ('pub', 'published'),
        ('drf', 'draft')
    )

    title = models.CharField(verbose_name='Title', max_length=100, blank=False)
    author = models.CharField(verbose_name='Author', max_length=50, blank=False)
    source = models.CharField(verbose_name='Source', max_length=100, blank=False)
    source_link = models.URLField(max_length=200, blank=True, null=True)
    text = RichTextField()
    datetime_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name='date edited', auto_now=True)
    image = models.ImageField(verbose_name='blog Image', upload_to='blog/blog_cover/', blank=False)
    # likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    status = models.CharField(verbose_name='Status', choices=STATUS_CHOICES, max_length=3)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])
