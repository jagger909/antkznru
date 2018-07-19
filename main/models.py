from django.db import models

# Create your models here.


class CallBack(models.Model):
    MessageText = models.CharField(max_length=200)
    TelephonNumber = models.CharField(max_length=200)
    PubDate = models.DateTimeField('date published')
    def __str__(self):
        return self.TelephonNumber