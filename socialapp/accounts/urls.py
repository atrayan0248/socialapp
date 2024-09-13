from django.urls import path

from socialapp.accounts.views import AddUserView

urlpatterns = [
    path('', AddUserView.as_view(), name='User Create'),
]
