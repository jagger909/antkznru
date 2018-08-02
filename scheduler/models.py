from django.db import models
from django.utils.crypto import get_random_string

from generic.choice_enum import ChoiceEnum
# Create your models here.

class Scheduler(models.Model):

    class TimeChoice(ChoiceEnum):
        T1 = "08:00-11:00"
        T2 = "10:00-13:00"
        T3 = "12:00-15:00"
        T4 = "14:00-17:00"
        T5 = "16:00-19:00"
        T6 = "18:00-21:00"
        # T7 = "20:00-23:00"

    sched_un_id = models.SlugField(db_index= True, unique=True, max_length=10)
    username = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=12)
    comment = models.CharField(max_length=200, blank=True)
    repair_date = models.DateField()
    repair_time = models.CharField(db_index= True, max_length=2, choices=TimeChoice.choices(), default=TimeChoice.T1)
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sched_un_id:
            # Newly created object, so set slug
            self.sched_un_id = get_random_string(length=10)

        super(Scheduler, self).save(*args, **kwargs)

    def getSchedFree(self):
        # TODO сделать толстыми модели и тонкими представления
        pass

    def __str__(self):
        return self.sched_un_id
