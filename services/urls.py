from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PaymentViewSet

router = SimpleRouter()
router.register('', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
