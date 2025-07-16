from django.urls import path, include

from core.apps.contracts.views import contract as contract_views
from core.apps.contracts.views import contract_side as contract_side_views


urlpatterns = [
    path('contract/', include(
        [
            path('create/', contract_views.ContractCreateApiView.as_view(), name='create-contract'),
            path('list/', contract_views.ContractListApiView.as_view(), name='list-contract'),
        ]
    )),
    path('contract_side/', include([
            path('create/', contract_side_views.ConstartSideCreateApiView.as_view(), name='contract-side-create'),
        ]
    ))
]