from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Div
from django.shortcuts import reverse
from django import forms
from .models import UserModel
from django.core.exceptions import ValidationError

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)


class AuthForm(AuthenticationForm):

    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, request=None, *args, **kwargs):
        super(AuthForm, self).__init__(request, *args, **kwargs)

        self.helper = FormHelper()

        self.fields['username'].widget.input_type = 'email'
        self.fields['username'].label = 'Email'

        self.helper.layout = Layout(
            Field("username", placeholder="Enter Email", autofocus=""),
            Field("password", placeholder="Enter Password"),
            HTML(
                '<a href="#">Forgot Password?</a>'
                #     .format(
                #     reverse("accounts:password-reset")
                # )
            ),
            Field("remember_me"),
            Submit("sign_in", "Log in", css_class="btn btn-primary"),
        )


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("email", placeholder="Enter Email", autofocus=""),
            Div(
                Div(
                    Field("first_name", placeholder="First Name", autofocus=""),
                    css_class="col-md-6"
                ),
                Div(
                    Field("last_name", placeholder="Last Name", autofocus=""),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Field("password1", placeholder="Enter Password"),
            Field("password2", placeholder="Enter Password"),
            Submit("sign_in", "Sign up", css_class="btn btn-primary"),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("Email already exist")
        return email

    def _post_clean(self):
        super(SignUpForm, self)._post_clean()
        self.clean_email()

    def save(self, commit=True):
        object = super(SignUpForm, self).save(False)
        object.username = object.email
        if commit:
            object.save()
        return object

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name')


class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("old_password", autofocus=""),
            Field("new_password1", autofocus=""),
            Field("new_password2", autofocus=""),
            Submit("change", "Change Password", css_class="btn btn-warning"),
        )


class UpdateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__( *args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("username", placeholder="Enter Email", autofocus=""),
            Field("first_name"),
            Field("last_name"),

            Submit("update", "Update", css_class="btn btn-primary"),
        )

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', "last_name")