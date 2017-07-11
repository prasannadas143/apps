from rest_framework import serializers
from appointmentscheduler.models import AppschedulerServices

class AppschedulerServicesSeriallizers(serializers.ModelSerializer):
    class Meta:
        model = AppschedulerServices
        fields = '__all__'


