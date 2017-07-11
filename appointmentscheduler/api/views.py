from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import  ListAPIView
from .serializers import AppschedulerServicesSeriallizers
from appointmentscheduler.models import AppschedulerServices

class ServicesListView(ListAPIView):
    queryset = AppschedulerServices.objects.all()
    serializer_class = AppschedulerServicesSeriallizers