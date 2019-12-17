from rest_framework import viewsets
from .models import Patent
from .serializers import PatentSerializer


# Create your views here.
class PatentViewSet(viewsets.ModelViewSet):
    model = Patent
    serializer_class = PatentSerializer
    queryset = Patent.objects.all()
