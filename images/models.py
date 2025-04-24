import uuid

from django.contrib.auth import get_user_model
from django.db import models

FORMAT_CHOICES = (
    ('JPEG', 'JPEG'),
    ('PNG', 'PNG'),
    ('WEBP', 'WEBP'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class ImageConversion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='image_conversions',
        null=True,
        blank=True
    )
    converted_image = models.ImageField(upload_to='images/')
    conversion_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.conversion_format} - {self.status}"
