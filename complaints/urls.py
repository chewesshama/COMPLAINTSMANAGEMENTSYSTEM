from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import (
    HomeView,
    UserRegistrationView,
    IndexView,
    UserLoginView,
    ProfileView,
    UserRegistrationDoneView,
    AllUserDisplayView,
    AllComplaintsDisplayView,
    DeleteUserView,
    PasswordChangeCustomView,
    PasswordChangeDoneView,
    UserComplaintsDisplayView,
    DeleteComplaintView,
    ComplaintDetailsView,
    RemarkAddedDone,
    RemarkDetailView,
    StaffUserProfileView,
    UpdateComplaintView,
    UpdateComplaintDoneView,
    UpdateRemarkView,
    DeleteRemarkView,
    userProfileUpdateView,
    add_complaint,
    add_remark,
    get_districts,
)


app_name = "complaints"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("home/", HomeView.as_view(), name="home"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("register-done/", UserRegistrationDoneView.as_view(), name="register_done"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("all-users/", AllUserDisplayView.as_view(), name="all_users_display"),
    path("staffs_user_profile_view/<int:pk>/", StaffUserProfileView.as_view(), name="staff_user_profile"),
    path(
        "all-complaints/",
        AllComplaintsDisplayView.as_view(),
        name="all_complaints_display",
    ),
    path("delete_complaint/<int:pk>/", DeleteComplaintView.as_view(), name="delete_complaint"),
    path("complaint_update/<int:pk>/", UpdateComplaintView.as_view(), name="update_complaint"),
    path("complaint_update_done/", UpdateComplaintDoneView.as_view(), name="complaint_update_done"),
    path(
        "user-complaints/",
        UserComplaintsDisplayView.as_view(),
        name="user_complaints_display",
    ),
    path("complaint/<int:pk>/", ComplaintDetailsView.as_view(), name="complaint_details"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("update/<int:pk>/", userProfileUpdateView, name="profile_update"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),
    path(
        "password_change/", PasswordChangeCustomView.as_view(), name="password_change"
    ),
    path(
        "password_change_done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("add-complaint/", add_complaint, name="add_complaint"),
    path('add_remark/<int:complaint_id>/', add_remark, name='add_remark'),
    path("add-remark-done/<int:pk>/", RemarkAddedDone.as_view(), name="remark_added_done"),
    path("remark_update/<int:pk>/", UpdateRemarkView.as_view(), name="remark_update"),
    path("delete_remark/<int:pk>/", DeleteRemarkView.as_view(), name="delete_remark"),
    path('remark/<int:pk>/', RemarkDetailView.as_view(), name='view_remark_details'),
    path("get_districts/", get_districts, name="get_districts"),
]

handler404 = "complaints.views.custom_404_view"
handler403 = "complaints.views.custom_403_view"
handler500 = "complaints.views.custom_500_view"
