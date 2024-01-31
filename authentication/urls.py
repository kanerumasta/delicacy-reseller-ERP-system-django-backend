from django.urls import path
from authentication.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('users', UserListView.as_view(), name='user_list'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('activate/<int:user_id>', AcceptUserView.as_view(), name='activate-user' ),
    path('deactivate/<int:user_id>', deactivate_user, name='deactivate-user' ),
    path('new-users',get_new_users )
]