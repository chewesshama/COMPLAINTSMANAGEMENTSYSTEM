from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import IntegerField
from django.db.models import Case, When, Value, CharField
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .forms import UserProfileForm, CEORegistrationForm, HODRegistrationForm, LoginForm, UserSearchForm, PasswordChangeCustomForm, AddComplaintForm
from .models import Complaint, User, ComplaintAttachments



def custom_404_view(request, exception=None):
    return render(request, 'error_templates/404.html', status=404)


def custom_403_view(request, exception=None):
    return render(request, 'error_templates/403.html', status=403)


def custom_500_view(request, exception=None):
    return render(request, 'error_templates/500.html', status=500)


def add_user_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        pass
    else:
        group.user_set.add(user)


class IndexView(TemplateView):
    template_name = 'complaints/index.html'


class HomeView(PermissionRequiredMixin, ListView):
    permission_required = 'complaints.add_complaint'
    model = Complaint
    template_name = 'complaints/home.html'
    context_object_name = 'complaints'


class UserLoginView(LoginView):
    username_field = 'email'
    template_name = 'complaints/login.html'
    authentication_form = LoginForm
    success_url = 'complaints:home'


class UserRegistrationView(PermissionRequiredMixin ,CreateView):
    permission_required = 'complaints.add_user'
    model = User
    template_name = 'complaints/user_registration_form.html'

    def get_form_class(self):
        for group in self.request.user.groups.all():
            user_type = group.name if self.request.user.is_authenticated else 'CEO'
            if user_type == 'CEO' or self.request.user.is_superuser:
                return CEORegistrationForm
            elif user_type == 'HOD':
                return HODRegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)

        user_groups = self.request.user.groups.all()

        if user_groups.exists():
            user_group = user_groups[0] 

        department = form.cleaned_data.get('department')

        user.save()

        if user_group and (user_group.name == 'CEO' or self.request.user.is_superuser):
            user.departments.set([department])
            group = form.cleaned_data.get('group')

            if group.name == 'CEO' or group.name == 'HOD':
                user.is_staff = True
                add_user_to_group(user, group)
                user.save()
            else:
                add_user_to_group(user, group)
                user.save()
        elif user_group and user_group.name == 'HOD':
            user.departments.set([self.request.user.departments.first()])
            user.groups.set([Group.objects.get(name='EMPLOYEE')])

        messages.success(self.request, 'User registered successfully.')
        return redirect('complaints:register_done')


class UserRegistrationDoneView(PermissionRequiredMixin,TemplateView):
    permission_required = 'complaints.add_user'
    template_name = 'complaints/user_register_done.html'


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'complaints/profile.html'
    context_object_name = 'user'

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
        return redirect('complaints:profile', pk = request.user.pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            user_pk = request.user.pk
            profile_url = reverse('complaints:profile', kwargs={'pk': user_pk})
            return redirect(profile_url)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'complaints/user_profile_update.html', context)


class DeleteUserView(PermissionRequiredMixin, DeleteView):
    permission_required = 'complaints.delete_user'
    model = User
    success_url = reverse_lazy('complaints:all_users_display')


class PasswordChangeCustomView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = 'complaints/password_change.html'
    success_url = reverse_lazy('complaints:password_change_done')

class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'complaints/password_change_done.html'


class AllUserDisplayView(PermissionRequiredMixin, ListView):
    permission_required = 'complaints.view_user'
    model = User
    template_name = 'complaints/all_users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_search_form'] = UserSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get('search_query')

        queryset = User.objects.annotate(
            order=Case(
                When(groups__name='CEO', then=Value(1)),
                When(groups__name='HOD', then=Value(2)),
                When(groups__name='EMPLOYEE', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )

        if user.groups.filter(name='HOD').exists():
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
        ).order_by('is_logged_in_user', 'order', 'username')

        if search_query:
            queryset = queryset.filter(Q(username__icontains=search_query) |
                                       Q(email__icontains=search_query) |
                                       Q(first_name__icontains=search_query) |
                                       Q(last_name__icontains=search_query))
        
        queryset = queryset.filter(is_superuser=False)
        return queryset


class AllComplaintsDisplayView(PermissionRequiredMixin, ListView):
    permission_required = 'complaints.view_user'
    model = Complaint
    template_name = 'complaints/all_complaints.html'
    context_object_name = 'complaints'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='CEO').exists() or user.is_superuser:
            queryset = Complaint.objects.all()
        elif user.groups.filter(name='HOD').exists():
            department = user.departments.first()
            if department:
                queryset = Complaint.objects.filter(targeted_department=department)
            else:
                queryset = Complaint.objects.none()
        else:
            queryset = Complaint.objects.none()

        return queryset


class UserComplaintsDisplayView(LoginRequiredMixin ,ListView):
    model = Complaint
    template_name = 'complaints/my_complaints.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        return Complaint.objects.filter(complainant=self.request.user).order_by('-date_added')


class ComplaintDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'complaints.view_user'
    model = Complaint
    template_name = 'complaints/complaint_details.html'
    context_object_name = 'complaints'


@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = AddComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)

            complaint = Complaint(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                complainant=request.user,
                targeted_department=form.cleaned_data['targeted_department'],
                targeted_personnel=form.cleaned_data['targeted_personnel'],
                status=form.cleaned_data['status'],
            )
            attachments = []
            picture = request.FILES.get('picture')
            video = request.FILES.get('video')
            voice = request.FILES.get('voice')
            file = request.FILES.get('file')
            
            if picture:
                attachments.append(ComplaintAttachments(picture=picture))
            if video:
                attachments.append(ComplaintAttachments(video=video))
            if voice:
                attachments.append(ComplaintAttachments(voice=voice))
            if file:
                attachments.append(ComplaintAttachments(file=file))

            complaint.save()

            complaint.attachments.set(attachments)

            return redirect('complaints:user_complaints_display')
    else:
        form = AddComplaintForm()

    context = {'form': form}
    return render(request, 'complaints/add_complaint_form.html', context)
