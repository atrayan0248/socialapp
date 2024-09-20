from django.urls import path

from socialapp.accounts.views import LoginView
from socialapp.accounts.views import LogoutView
from socialapp.accounts.views import UserView

urlpatterns = [
    path('', UserView.as_view(), name='User API'),
    path('login', LoginView.as_view(), name='Auth Login API'),
    path('logout', LogoutView.as_view(), name='Auth Logout API'),
    # path('details', UserDetailsView.as_view(), name='User Details API')
]
