from rest_framework import routers
from patent.views import PatentViewSet
router = routers.DefaultRouter()
router.register(r'patents', PatentViewSet, basename='patent')
