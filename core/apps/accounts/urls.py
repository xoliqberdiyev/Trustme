from django.urls import path, include

from core.apps.accounts.views.auth import LoginApiView, RegisterApiView

urlpatterns = [
    path('auth/', include(
        [
            path('login/', LoginApiView.as_view(), name='login'),
            path('register/', RegisterApiView.as_view(), name='login'),
        ]
    ))
]