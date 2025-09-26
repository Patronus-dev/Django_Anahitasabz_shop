from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteContactInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    phone_number = models.CharField(
        max_length=10,
        verbose_name=_("Phone Number"),
        help_text=_("Enter your phone number")
    )
    instagram_id = models.CharField(verbose_name=_("Instagram Id"), blank=True, null=True)
    whatsapp_number = models.IntegerField(verbose_name=_("WhatsApp Number"),
                                          help_text=_("Enter your phone number without 0"), blank=True, null=True)
    telegram_id = models.URLField(verbose_name=_("Telegram Id"), blank=True, null=True)

    class Meta:
        verbose_name = _("Site Contact Info")
        verbose_name_plural = _("Site Contact Info")

    def __str__(self):
        return self.name
