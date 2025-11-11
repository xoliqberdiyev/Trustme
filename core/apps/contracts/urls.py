from django.urls import path, include

from core.apps.contracts.views import contract as contract_views
from core.apps.contracts.views import contract_side as contract_side_views
from core.apps.contracts.views import contract_signature as contract_signature_views
from core.apps.contracts.views import folder as folder_views

urlpatterns = [
    path('contract/', include(
        [
            path('create/', contract_views.ContractCreateApiView.as_view(), name='create-contract'),
            path('list/', contract_views.ContractListApiView.as_view(), name='list-contract'),
            path('<uuid:id>/', contract_views.ContractDetailApiView.as_view(), name='detail-contract'),
            path('<uuid:id>/update/', contract_views.ContractUpdateApiView.as_view()),
        ]
    )),
    path('contract_side/', include([
            path('create/', contract_side_views.ContractSideCreateApiView.as_view(), name='contract-side-create'),
        ]
    )),
    path('contract_signature/', include(
        [
            path('send_signature_code/<uuid:signature_id>/', contract_signature_views.SendContractSignatureCodeApiView.as_view(), name='send-signature-code'),
            path('sign_contract/', contract_signature_views.SigningContractApiView.as_view(), name='sign-contract'),
        ]
    )),
    path('folder/', include(
        [
            path('list/', folder_views.FolderListApiView.as_view()),
            path('create/', folder_views.FolderCreateApiView.as_view()),
            path('<uuid:folder_id>/update/', folder_views.FolderUpdateApiView.as_view()),
            path('<uuid:id>/contracts/', folder_views.ContractListApiView.as_view()),
        ]
    )),
]