import os
import requests
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def logout_view(request):
    messages.info(request, _("See you later"))
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException(_("Can't get access token"))
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    name = username if name is None else name
                    email = profile_json.get("email")
                    email = name if email is None else email
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(
                        request, _("Welcome back! {}").format(user.first_name)
                    )
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException(_("Can't get your profile"))
        else:
            raise GithubException(_("Can't get code"))
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException(_("Can't get authorization code."))
        ACCESS_TOKEN = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )
        profile_json = profile_request.json()
        properties = profile_json.get("kakao_account").get("profile")
        nickname = properties.get("nickname", None)
        email = profile_json.get("kakao_account").get("email", None)
        email = nickname if email is None else email
        profile_image = (
            profile_json.get("kakao_account", None)
            .get("profile", None)
            .get("profile_image_url", None)
        )
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(
                    _("Please log in with:{}").format(user.login_method)
                )
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)

                user.avatar.save(
                    f"{nickname}-avatar.jpeg", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, _("Welcome back! {}").format(user.first_name))
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def line_login(request):
    client_id = os.environ.get("LINE_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/line/callback"
    state = "line2350"
    return redirect(
        f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope=profile"
    )


class LineException(Exception):
    pass


def line_callback(request):
    try:
        code = request.GET.get("code")
        uri_access_token = "https://api.line.me/oauth2/v2.1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data_programs = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/users/login/line/callback",
            "client_id": os.environ.get("LINE_ID"),
            "client_secret": os.environ.get("LINE_SECRET"),
        }
        response_post = requests.post(
            uri_access_token,
            headers=headers,
            data=data_programs,
        )

        token_json = response_post.json()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.line.me/v2/profile",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        nickname = profile_json.get("displayName", "")
        email = profile_json.get("displayName", "")
        profile_image = profile_json.get("pictureUrl", None)
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_LINE:
                raise LineException(
                    _("Please log in with {}").format(user.login_method)
                )
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_LINE,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar.jpeg", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, _("welcome back! {}").format(user.first_name))
        return redirect(reverse("core:home"))
    except LineException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = _("Profile Updated")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": _("First name")}
        form.fields["last_name"].widget.attrs = {"placeholder": _("Last name")}
        form.fields["bio"].widget.attrs = {"placeholder": _("Bio")}
        form.fields["birthdate"].widget.attrs = {"placeholder": _("Birthdate")}
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {
            "placeholder": _("Current Password")
        }
        form.fields["new_password1"].widget.attrs = {"placeholder": _("New password")}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": _("Confirm new password")
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        if translation.LANGUAGE_SESSION_KEY in request.session:
            del request.session[translation.LANGUAGE_SESSION_KEY]
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
