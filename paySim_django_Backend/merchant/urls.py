from merchant.views import MerchantViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'merchants', MerchantViewSet, basename='merchant')
urlpatterns = router.urls

