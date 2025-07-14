from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include(
        [
            path('', include('core.apps.accounts.urls')),
        ]
    )),
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
