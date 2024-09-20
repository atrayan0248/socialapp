from django.urls import path

from socialapp.user_details.views import UserDetailsView

urlpatterns = [
    path('', UserDetailsView.as_view(), name='User Details API'),
]
