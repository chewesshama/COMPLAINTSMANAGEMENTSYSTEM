from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView
)
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import IntegerField
from django.db.models import Case, When, Value, CharField
from django.db.models import Q, Subquery
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, Http404
from mtaa import tanzania
from .models import Complaint, Remark, User, ComplaintAttachments
from .forms import (
    UserProfileForm,
    CEORegistrationForm,
    HODRegistrationForm,
    LoginForm,
    SearchForm,
    PasswordChangeCustomForm,
    AddComplaintForm,
    UpdateComplaintForm,
    AddRemarkForm,
    UpdateRemarkForm,
)
from django.db import transaction


def get_districts(request):
    region_name = request.GET.get("region_name")

    if hasattr(tanzania, region_name):
        region = getattr(tanzania, region_name)

        if hasattr(region, "districts"):
            districts = region.districts
            district_names = [district for district in districts]
            return JsonResponse(district_names, safe=False)

    return JsonResponse([], safe=False)


def custom_404_view(request, exception=None):
    return render(request, "error_templates/404.html", status=404)


def custom_403_view(request, exception=None):
    return render(request, "error_templates/403.html", status=403)


def custom_500_view(request, exception=None):
    return render(request, "error_templates/500.html", status=500)


def add_user_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        pass
    else:
        group.user_set.add(user)


class IndexView(TemplateView):
    template_name = "complaints/index.html"


class HomeView(PermissionRequiredMixin, ListView):
    permission_required = "complaints.add_complaint"
    model = Complaint
    template_name = "complaints/home.html"
    context_object_name = "complaints"


class UserLoginView(LoginView):
    username_field = "email"
    template_name = "complaints/login.html"
    authentication_form = LoginForm
    success_url = "complaints:home"


class UserRegistrationView(PermissionRequiredMixin, CreateView):
    permission_required = "complaints.add_user"
    model = User
    template_name = "complaints/user_registration_form.html"

    def get_form_class(self):
        for group in self.request.user.groups.all():
            user_type = group.name if self.request.user.is_authenticated else "CEO"
            if user_type == "CEO" or self.request.user.is_superuser:
                return CEORegistrationForm
            elif user_type == "HOD":
                return HODRegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)

        user_groups = self.request.user.groups.all()

        if user_groups.exists():
            user_group = user_groups[0]

        department = form.cleaned_data.get("department")

        user.save()

        if user_group and (user_group.name == "CEO" or self.request.user.is_superuser):
            user.departments.set([department])
            group = form.cleaned_data.get("group")

            if group.name == "CEO" or group.name == "HOD":
                user.is_staff = True
                add_user_to_group(user, group)
                user.save()
            else:
                add_user_to_group(user, group)
                user.save()
        elif user_group and user_group.name == "HOD":
            user.departments.set([self.request.user.departments.first()])
            user.groups.set([Group.objects.get(name="EMPLOYEE")])

        messages.success(self.request, "User registered successfully.")
        return redirect("complaints:register_done")


class UserRegistrationDoneView(PermissionRequiredMixin, TemplateView):
    permission_required = "complaints.add_user"
    template_name = "complaints/user_register_done.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "complaints/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user

        context["user_details"] = user_profile
        return context


@login_required
def userProfileUpdateView(request, pk):
    user_profile = get_object_or_404(User, pk=pk)

    if request.user.username != user_profile.username:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect("complaints:profile", pk=request.user.pk)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            user_pk = request.user.pk
            profile_url = reverse("complaints:profile", kwargs={"pk": user_pk})
            return redirect(profile_url)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "form": form,
    }

    return render(request, "complaints/user_profile_update.html", context)


class DeleteUserView(PermissionRequiredMixin, DeleteView):
    permission_required = "complaints.delete_user"
    model = User
    success_url = reverse_lazy("complaints:all_users_display")


class PasswordChangeCustomView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = "complaints/password_change.html"
    success_url = reverse_lazy("complaints:password_change_done")


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "complaints/password_change_done.html"


class AllUserDisplayView(PermissionRequiredMixin, ListView):
    permission_required = "complaints.view_user"
    template_name = "complaints/all_users.html"
    model = User
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_search_form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get("search_query")

        queryset = User.objects.annotate(
            order=Case(
                When(groups__name="CEO", then=Value(1)),
                When(groups__name="HOD", then=Value(2)),
                When(groups__name="EMPLOYEE", then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )

        if user.groups.filter(name="HOD").exists():
            department = user.departments.first()
            if department:
                queryset = queryset.exclude(departments=None)
                queryset = queryset.filter(Q(departments=department) | Q(pk=user.pk))
            else:
                queryset = queryset.filter(pk=user.pk)

        queryset = queryset.annotate(
            is_logged_in_user=Case(
                When(pk=user.pk, then=Value(0)),
                default=Value(1),
                output_field=CharField(),
            )
        ).order_by("is_logged_in_user", "order", "username")

        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        queryset = queryset.filter(is_superuser=False)
        return queryset


class AllComplaintsDisplayView(PermissionRequiredMixin, ListView):
    permission_required = "complaints.view_user"
    model = Complaint
    template_name = "complaints/all_complaints.html"
    context_object_name = "complaints"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_search_form"] = SearchForm(self.request.GET)

        queryset = self.get_queryset()

        complaint = queryset.first()

        remarks = complaint.remarks.all() if complaint else []

        latest_remark = remarks.last()
        latest_status = (
            latest_remark.status
            if latest_remark
            else complaint.status
            if complaint
            else None
        )

        context["remarks"] = remarks
        context["latest_status"] = latest_status
        return context

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get("search_query")

        if user.groups.filter(name="CEO").exists() or user.is_superuser:
            queryset = Complaint.objects.all()
        elif user.groups.filter(name="HOD").exists():
            department = user.departments.first()
            if department:
                queryset = Complaint.objects.filter(targeted_department=department)
            else:
                queryset = Complaint.objects.none()
        else:
            queryset = Complaint.objects.none()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(complainant__username__icontains=search_query)
                | Q(targeted_department__name__icontains=search_query)
                | Q(targeted_personnel__username__icontains=search_query)
            )

        return queryset


class UserComplaintsDisplayView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = "complaints/my_complaints.html"
    context_object_name = "complaints"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_search_form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        print("Search Query:", search_query)

        user_remarks_subquery = Remark.objects.filter(
            remark_targeted_personnel=self.request.user
        ).values("complaint_id")

        queryset = Complaint.objects.filter(
            Q(complainant=self.request.user)
            | Q(targeted_personnel=self.request.user)
            | Q(id__in=Subquery(user_remarks_subquery))
        ).order_by("-date_added")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(complainant__username__icontains=search_query)
                | Q(targeted_department__name__icontains=search_query)
                | Q(targeted_personnel__username__icontains=search_query)
            )
            print("Filtered Queryset Count:", queryset.count())

        return queryset


class DeleteComplaintView(PermissionRequiredMixin, DeleteView):
    permission_required = "complaints.delete_complaint"
    model = Complaint
    success_url = reverse_lazy("complaints:user_complaints_display")


class UpdateComplaintView(PermissionRequiredMixin, UpdateView):
    permission_required = 'complaints.change_complaint'
    model = Complaint
    form_class = UpdateComplaintForm
    template_name = 'complaints/update_complaint_form.html'
    context_object_name = 'complaint'

    def get_success_url(self):
        return reverse_lazy('complaints:complaint_details', kwargs={'pk': self.object.pk})


class UpdateComplaintDoneView(PermissionRequiredMixin, TemplateView):
    permission_required = 'complaint.change_complaint'
    template_name = 'complaint/complaint_update_done.html'


class ComplaintDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "complaints.view_complaint"
    model = Complaint
    template_name = "complaints/complaint_details.html"
    context_object_name = "complaint"

    def get_object(self, queryset=None):
        complaint = super().get_object(queryset=queryset)
        user = self.request.user

        if (
            user == complaint.complainant
            or user == complaint.targeted_personnel
            or user.is_superuser
            or Remark.objects.filter(complaint=complaint, remark_targeted_personnel=user).exists()
        ):
            return complaint
        elif user.groups.filter(name='CEO').exists():
            return complaint
        else:
            raise Http404("You are not allowed to view this complaint.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint = self.get_object()
        remarks = complaint.remarks.all()

        latest_remark = remarks.last()
        latest_status = latest_remark.status if latest_remark else complaint.status

        context["remarks"] = remarks
        context["latest_status"] = latest_status
        return context


@login_required
def add_complaint(request):
    if request.method == "POST":
        form = AddComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            attachment_type = form.cleaned_data["attachment_type"]
            attachments = []

            if attachment_type == "picture":
                picture = request.FILES.get("picture")
                if picture:
                    attachment = ComplaintAttachments(picture=picture)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "voice":
                voice = request.FILES.get("voice")
                if voice:
                    attachment = ComplaintAttachments(voice=voice)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "video":
                video = request.FILES.get("video")
                if video:
                    attachment = ComplaintAttachments(video=video)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "file":
                file = request.FILES.get("file")
                if file:
                    attachment = ComplaintAttachments(file=file)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "all":
                picture = request.FILES.get("picture")
                video = request.FILES.get("video")
                voice = request.FILES.get("voice")
                file = request.FILES.get("file")

                if picture:
                    attachment = ComplaintAttachments(picture=picture)
                    attachment.save()
                    attachments.append(attachment)
                if video:
                    attachment = ComplaintAttachments(video=video)
                    attachment.save()
                    attachments.append(attachment)
                if voice:
                    attachment = ComplaintAttachments(voice=voice)
                    attachment.save()
                    attachments.append(attachment)
                if file:
                    attachment = ComplaintAttachments(file=file)
                    attachment.save()
                    attachments.append(attachment)

            complaint = Complaint(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                complainant=request.user,
                targeted_department=form.cleaned_data["targeted_department"],
                targeted_personnel=form.cleaned_data["targeted_personnel"],
                status="Opened",
            )

            complaint.save()
            complaint.attachments.set(attachments)
            return redirect("complaints:user_complaints_display")

    else:
        form = AddComplaintForm()

    context = {"form": form}
    return render(request, "complaints/add_complaint_form.html", context)


@login_required
def add_remark(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    if request.method == "POST":
        form = AddRemarkForm(
            request.POST, request.FILES, initial={"complaint": complaint}
        )
        if form.is_valid():
            attachment_type = form.cleaned_data["attachment_type"]
            attachments = []

            if attachment_type == "picture":
                picture = request.FILES.get("picture")
                if picture:
                    attachment = ComplaintAttachments(picture=picture)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "voice":
                voice = request.FILES.get("voice")
                if voice:
                    attachment = ComplaintAttachments(voice=voice)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "video":
                video = request.FILES.get("video")
                if video:
                    attachment = ComplaintAttachments(video=video)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "file":
                file = request.FILES.get("file")
                if file:
                    attachment = ComplaintAttachments(file=file)
                    attachment.save()
                    attachments.append(attachment)
            elif attachment_type == "all":
                picture = request.FILES.get("picture")
                video = request.FILES.get("video")
                voice = request.FILES.get("voice")
                file = request.FILES.get("file")

                if picture:
                    attachment = ComplaintAttachments(picture=picture)
                    attachment.save()
                    attachments.append(attachment)
                if video:
                    attachment = ComplaintAttachments(video=video)
                    attachment.save()
                    attachments.append(attachment)
                if voice:
                    attachment = ComplaintAttachments(voice=voice)
                    attachment.save()
                    attachments.append(attachment)
                if file:
                    attachment = ComplaintAttachments(file=file)
                    attachment.save()
                    attachments.append(attachment)

            remark = Remark(
                complaint=form.cleaned_data["complaint"],
                content=form.cleaned_data["content"],
                respondent=request.user,
                remark_targeted_department=form.cleaned_data[
                    "remark_targeted_department"
                ],
                remark_targeted_personnel=form.cleaned_data[
                    "remark_targeted_personnel"
                ],
                status=form.cleaned_data["status"],
            )

            remark.save()
            remark.attachments.set(attachments)

            complaint = form.cleaned_data["complaint"]

            url = reverse("complaints:remark_added_done", args=[complaint.pk])
            return redirect(url)
    else:
        form = AddRemarkForm(initial={"complaint": complaint})

    context = {"form": form}
    return render(request, "complaints/add_remark.html", context)


class RemarkAddedDone(LoginRequiredMixin, DetailView):
    model = Complaint
    context_object_name = "complaint"
    template_name = "complaints/remark_add_done.html"


class RemarkDetailView(LoginRequiredMixin, DetailView):
    model = Remark
    template_name = "complaints/remark_details.html"
    context_object_name = "remark"


class UpdateRemarkView(PermissionRequiredMixin, UpdateView):
    permission_required = 'complaints.change_remark'
    model = Remark
    form_class = UpdateRemarkForm
    template_name = 'complaints/update_remark_form.html'
    context_object_name = 'remark'
    
    def get_object(self, queryset=None):
        remark = super().get_object(queryset=queryset)
        user = self.request.user

        if (
            user == remark.respondent
        ):
            return remark
        else:
            raise Http404("You are not allowed to view this remark.")

    def get_success_url(self):
        return reverse_lazy('complaints:complaint_details', kwargs={'pk': self.object.pk})


class DeleteRemarkView(PermissionRequiredMixin, DeleteView):
    permission_required = "complaints.delete_remark"
    model = Remark

    def get_success_url(self):
            complaint = self.object.complaint 
            return reverse_lazy('complaints:complaint_details', kwargs={'pk': complaint.pk})

class StaffUserProfileView(PermissionRequiredMixin, DetailView):
    permission_required = "complaints.view_user"
    model = User
    template_name = "complaints/users_profile.html"
    context_object_name = "user"
