from django.db import models

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_name = models.CharField(max_length=200)
    extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=50)
    size_bytes = models.PositiveBigIntegerField()
    sha256 = models.CharField(max_length=64)
    is_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name
