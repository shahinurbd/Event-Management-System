from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import CustomRegistrationForm,LoginForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetConfirmForm,CustomPasswordResetForm,EditProfileForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView

User = get_user_model()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()



class SignUpView(FormView):
    template_name = "registration/register.html"
    form_class = CustomRegistrationForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        messages.success(self.request, 'A Confirmation mail has been sent.Please check your email.')
        return super().form_valid(form)



class CustomLoginView(LoginView):

    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

    

    
class ActiveUser(View):

    def get(self, request, user_id,token, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active=True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse("Invalid id or token")
        except:
            return HttpResponse("User not found")



class AssignRole(LoginRequiredMixin,UserPassesTestMixin,View):

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {"form": form})
    
    def post(self, request, user_id, *args, **kwargs):
        if request.method == "POST":
            user = User.objects.get(id=user_id)
            form = AssignRoleForm(request.POST)
            if form.is_valid():
                role = form.cleaned_data.get('role')
                user.groups.clear()
                user.groups.add(role)
                messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
                return redirect('admin-dashboard')



class CreateGroup(LoginRequiredMixin,UserPassesTestMixin,View):

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get(self, request, *args, **kwargs):
        form = CreateGroupForm()
        return render(request, 'admin/create_group.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CreateGroupForm(request.POST)

            if form.is_valid():
                group = form.save()
                messages.success(request, f"Group {group.name} has been created successfully")
                return redirect('create-group')



class GroupList(LoginRequiredMixin,UserPassesTestMixin,ListView):

    model = User
    context_object_name = "groups"
    template_name = "admin/group_list.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get_queryset(self):
        groups = Group.objects.prefetch_related('permissions').all()
        return groups


    

class DeleteGroup(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    def test_func(self):
        return self.request.user.groups.filter(name="Admin").exists()
    def handle_no_permission(self):
        return redirect('no-permission')
    
    model = Group
    success_url = reverse_lazy('group-list')
    pk_url_kwarg = 'id'
    context_object_name = 'admin/group_list.html'


class ProfileView(LoginRequiredMixin,TemplateView):

    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['profile_image'] = user.profile_image
        context['phone_number'] = user.phone_number
        context['bio'] = user.bio
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context
    

class ChangePassword(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'A Reset email sent. Please check your email.')
        return super().form_valid(form)
    

class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, 'Password Reset Successfully.')
        return super().form_valid(form)
    

class EditProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')
    
    
    


