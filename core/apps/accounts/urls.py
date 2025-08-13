from django.urls import path, include

from core.apps.accounts.views.auth import LoginApiView, RegisterApiView, ConfirUserApiView, ChoiceUserRoleApiView, SearchUserPhoneApiView

urlpatterns = [
    path('auth/', include(
        [
            path('login/', LoginApiView.as_view(), name='login'),
            path('register/', RegisterApiView.as_view(), name='register'),
            path('confirm_user/', ConfirUserApiView.as_view(), name='confirm-user'),
            path('choise_user_role/', ChoiceUserRoleApiView.as_view(), name='choise-user-role'),
        ]
    )),
    path('user/', include(
        [
            path('<str:number>/search/', SearchUserPhoneApiView.as_view()),
        ]
    ))
]