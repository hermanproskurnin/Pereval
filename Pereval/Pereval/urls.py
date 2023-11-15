from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from pick.views import PerevalViewSet, EmailAPIView

router = routers.DefaultRouter()
router.register(r'pereval', PerevalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/submitData/', include(router.urls)),
    path('api/submitData/user__email=<str:email>', EmailAPIView.as_view(), name='email-pereval'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

