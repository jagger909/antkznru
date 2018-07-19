from rest_framework import serializers
from scheduler.models import Scheduler


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scheduler
        fields = ('username', 'honeypot', 'adres', 'telephone', 'comment', 'repair_date', 'repair_time')