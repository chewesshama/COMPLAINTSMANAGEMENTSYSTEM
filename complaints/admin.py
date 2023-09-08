from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Complaint, Department, Remark, ComplaintAttachments

class CustomUserAdmin(UserAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if 'CEO' in [group.name for group in obj.groups.all()] or 'HOD' in [group.name for group in obj.groups.all()]:
            obj.is_staff = True
            obj.save()

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Complaint)
admin.site.register(Remark)
admin.site.register(ComplaintAttachments)
