from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Blog(models.Model):
    """
    A very simple blog to contain articles.

    Attributes:
        title (models.CharField): Required unique title string.
    """
    title = models.CharField(
        _("title"),
        blank=False,
        max_length=55,
        default="",
        unique=True,
    )

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return absolute URL to the blog detail view.

        Returns:
            string: An URL.
        """
        return reverse("cotton_bootstrap:blog-detail", args=[
            str(self.id)
        ])
