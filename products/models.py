from django.db import models
from django.utils.translation import gettext_lazy as _


class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Keyword"))

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Product Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    price = models.PositiveIntegerField(default=0, verbose_name=_("Price"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    keywords = models.ManyToManyField(Keyword, blank=True, verbose_name=_("Keywords"))

    cover = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name=_("Cover Image"))
    image1 = models.ImageField(upload_to="products/gallery/", blank=True, null=True, verbose_name=_("Image 1"))
    image2 = models.ImageField(upload_to="products/gallery/", blank=True, null=True, verbose_name=_("Image 2"))
    image3 = models.ImageField(upload_to="products/gallery/", blank=True, null=True, verbose_name=_("Image 3"))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title

    def get_images(self):
        images = []
        if self.cover:
            images.append(self.cover.url)
        if self.image1:
            images.append(self.image1.url)
        if self.image2:
            images.append(self.image2.url)
        if self.image3:
            images.append(self.image3.url)
        return images
