from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import HomeView, UserRegistrationView, IndexView, UserLoginView, userProfileUpdateView, ProfileView, UserRegistrationDoneView, AllUserDisplayView, AllComplaintsDisplayView, DeleteUserView, PasswordChangeCustomView, PasswordChangeDoneView


app_name = "complaints"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("home/", HomeView.as_view(), name="home"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("register-done/", UserRegistrationDoneView.as_view(), name="register_done"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("all-users/", AllUserDisplayView.as_view(), name="all_users_display"),
    path("all-complaints/", AllComplaintsDisplayView.as_view(), name="all_complaints_display"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("update/<int:pk>/", userProfileUpdateView, name="profile_update"),
    path('delete_user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('password_change/', PasswordChangeCustomView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

]

