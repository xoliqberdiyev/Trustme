from django.urls import path, include

from core.apps.accounts.views.auth import LoginApiView, RegisterApiView, ConfirUserApiView, ChoiceUserRoleApiView, CompliteUserProfileApiView

urlpatterns = [
    path('auth/', include(
        [
            path('login/', LoginApiView.as_view(), name='login'),
            path('register/', RegisterApiView.as_view(), name='login'),
            path('confirm_user/', ConfirUserApiView.as_view(), name='confirm-user'),
            path('choise_user_role/', ChoiceUserRoleApiView.as_view(), name='choise-user-role'),
            path('complite_user_profile/<str:phone>/', CompliteUserProfileApiView.as_view(), name='complite-user-profile'),
        ]
    ))
]