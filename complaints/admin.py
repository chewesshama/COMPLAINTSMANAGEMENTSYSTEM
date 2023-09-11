from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Complaint, Department, Remark, ComplaintAttachments


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("User details", {
            "fields": [
                "username",
                "first_name",
                "last_name",
                "email",
                "is_superuser",
                "is_staff",
                "departments",
                "profile_picture",
                "phone_number",
                "location",
            ],
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Complaint)
admin.site.register(Remark)
admin.site.register(ComplaintAttachments)


admin.site.site_header = 'CMS admin area'
admin.site.site_title = 'CMS admin site'


