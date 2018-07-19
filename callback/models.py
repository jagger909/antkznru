from django.db import models

# Create your models here.

class Zayavka(models.Model):
    class Meta():
        db_table = 'zayavka'

    zayavka_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=12)
    zayavka_text = models.TextField(max_length=100)

    def __str__(self):
        return self.name