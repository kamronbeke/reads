from django.urls import path

from users.views import (follow_user, unfollow_user, ProfileView, RegisterView, LoginView, \
                         LogoutView, user_profile, UserListView, UpdateProfileView)

app_name = 'users'

urlpatterns = [
    path('user/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('profile/', ProfileView.as_view(), name='profile_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),   name='logout'),



    # path('profile/', ProfileView.as_view(), name='profile'),

    path('user_detail/<int:user_id>/', user_profile, name='user_detail'),
    path('users_list/', UserListView.as_view(), name='user_list'),


    path('update/', UpdateProfileView.as_view(), name='update')
]