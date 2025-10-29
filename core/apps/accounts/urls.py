from django.urls import path, include

from core.apps.accounts.views.auth import LoginApiView, RegisterApiView, ConfirUserApiView, ChoiceUserRoleApiView, SearchUserPhoneApiView
from core.apps.accounts.views.forgot_password import ConfirmCodeApiView, SendCodeApiView, ResetPasswordApiView

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
    )),
    path('forgot_password/', include(
        [
            path('send_code/', SendCodeApiView.as_view()),
            path('forgot_password/', ConfirmCodeApiView.as_view()),
            path('reset_password/', ResetPasswordApiView.as_view()),
        ]
    )),
]