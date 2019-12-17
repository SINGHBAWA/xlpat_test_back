from rest_framework import viewsets, pagination,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patent
from .serializers import PatentSerializer
import requests
from bs4 import BeautifulSoup

# Create your views here.
class PatentViewSet(viewsets.ModelViewSet):
    model = Patent
    serializer_class = PatentSerializer
    queryset = Patent.objects.all()

    @action(detail=False)
    def details(self, request):
        print(self, request.GET)
        policy_number = request.GET.get('policy_number')
        if not policy_number:
            return Response({"description": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        patent_page_url_string = 'https://patents.google.com/patent/{patent}/en'\
            .format(patent=policy_number)

        url = patent_page_url_string.format(patent=policy_number)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        description = soup.find("section", attrs={"itemprop": "description"})
        if not description:
            return Response({"description": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"description": str(description)}, status=status.HTTP_200_OK)

