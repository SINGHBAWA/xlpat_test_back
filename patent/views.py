from rest_framework import viewsets, pagination,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patent
from .serializers import PatentSerializer
import requests
from bs4 import BeautifulSoup
from django.conf import settings


# Create your views here.
class PatentViewSet(viewsets.ModelViewSet):
    model = Patent
    serializer_class = PatentSerializer
    queryset = Patent.objects.all()

    @action(detail=False)
    def details(self, request):
        policy_number = request.GET.get('policy_number')
        if not policy_number:
            return Response({"description": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        url = settings.GP_PATENT_PAGE_URL.format(patent=policy_number)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        description = soup.find("section", attrs={"itemprop": "description"})
        if not description:
            return Response({"description": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"description": str(description)}, status=status.HTTP_200_OK)

    @action(detail=False)
    def full_text_search(self, request):
        print(settings.GP_FULL_TEXT_SEARCH_URL)
        policy_number = request.GET.get('policy_number')
        if not policy_number:
            return Response({"description": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        url = settings.GP_FULL_TEXT_SEARCH_URL.format(
            policy_number=policy_number
        )

        r = requests.get(url)
        r_json = r.json()
        results = r_json.get("results")
        return Response({"search_results": results}, status=status.HTTP_200_OK)
