from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    STATUS_CHOICES = (
        ('pub', _('Published')),
        ('drf', _('Draft')),
    )

    title = models.CharField(verbose_name=_('Title'), max_length=100, blank=False)
    author = models.CharField(verbose_name=_('Author'), max_length=50, blank=False)
    source = models.CharField(verbose_name=_('Source'), max_length=100, blank=False)
    source_link = models.URLField(verbose_name=_('Source link'), max_length=200, blank=True, null=True)
    text = RichTextField(verbose_name=_('Text'))

    status = models.CharField(verbose_name=_('Status'), choices=STATUS_CHOICES, max_length=3)
    datetime_created = models.DateTimeField(verbose_name=_('Date created'), auto_now_add=True)
    datetime_modified = models.DateTimeField(verbose_name=_('Date edited'), auto_now=True)
    image = models.ImageField(verbose_name=_('Blog image'), upload_to='blog/blog_cover/', blank=False)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    @staticmethod
    def resize_image(image):
        """Resize image to 390x390"""
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile

        img = Image.open(image)
        img = img.convert('RGB')
        img = img.resize((390, 390), Image.Resampling.LANCZOS)

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)

        return InMemoryUploadedFile(
            thumb_io,
            field_name=None,
            name=image.name,
            content_type='image/jpeg',
            size=thumb_io.getbuffer().nbytes,
            charset=None
        )
