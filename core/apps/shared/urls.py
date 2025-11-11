from django.urls import path

from core.apps.shared.views.contact_us import ContactUsApiView


urlpatterns = [
    path('contact_us/', ContactUsApiView.as_view()),
]