from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms/', include('lms.urls', namespace='lms')),
    path('users/', include('users.urls', namespace='users')),

    path('spectacular/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc-ui'),
]
