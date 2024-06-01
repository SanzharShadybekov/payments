from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from accounts.views import UserViewSet, PasswordResetViewSet

router = SimpleRouter()
router.register('', UserViewSet)
router.register('password', PasswordResetViewSet)

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('refresh/', views.RefreshView.as_view()),
    path('', include(router.urls)),
]
