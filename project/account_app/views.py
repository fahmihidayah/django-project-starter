from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    authenticate,
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.views.generic import TemplateView, CreateView, UpdateView
from .forms import AuthForm, SignUpForm, UpdateUserForm, UserPasswordChangeForm, UpdateProfileForm
from .models import UserModel
from django.conf import settings
from .repositories import ProfileRepository
# Create your views here.


class AccountLoginView(LoginView):
    template_name = 'account_app/registration/login.html'
    form_class = AuthForm

    def get_success_url(self):
        return reverse('account_profile')

    def form_valid(self, form):
        redirect = super().form_valid(form)
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me is True:
            ONE_MONTH = 30 * 24 * 60 * 60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)
        return redirect


class AccountLogoutView(LogoutView):
    template_name = 'account_app/registration/logged_out.html'


class AccountProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = UpdateUserForm
    template_name = "account_app/account_profile.html"
    profile_repository = ProfileRepository()

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountProfileView, self).get_context_data(**kwargs)
        if 'profile_form' not in kwargs:
            context['profile_form'] = UpdateProfileForm(
                instance=self.profile_repository.get_user_profile(self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form: UpdateProfileForm = UpdateProfileForm(data=self.request.POST,
                                                            instance=self.profile_repository.get_user_profile(
                                                                self.request.user))
        if form.is_valid() and profile_form.is_valid():
            profile_form.save()
            return self.form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

    def get_success_url(self):
        messages.success(self.request, 'Profile updated')
        return reverse('account_profile')


class UserChangePasswordView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'account_app/registration/password_change_form.html'


class PasswordChangeDoneView(TemplateView):
    template_name = 'account_app/registration/password_change_done.html'


class SignUpView(CreateView):
    model = UserModel
    form_class = SignUpForm
    template_name = 'account_app/registration/sign_up.html'

    def get_success_url(self):
        return reverse('index')
