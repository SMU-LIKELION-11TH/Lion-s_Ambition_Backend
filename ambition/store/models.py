from django.db import models

class Order(models.Model):
    id = models.IntegerField()
    status = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)],)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
