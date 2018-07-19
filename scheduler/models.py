from django.db import models
from generic.choice_enum import ChoiceEnum
from enum import Enum
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

    username = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    telephone = models.IntegerField()
    comment = models.CharField(max_length=200, blank=True)
    repair_date = models.DateField()
    repair_time = models.CharField(max_length=2, choices=TimeChoice.choices(), default=TimeChoice.T1)
    pub_date = models.DateTimeField(auto_now_add=True)
    sched_un_id = models.CharField(db_index= True, unique=True, max_length=10)

    def __str__(self):
        return self.address
