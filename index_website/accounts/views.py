from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from . import models
from . import forms
from mixins.forms.multiforms import MultiFormsView, MultiFormsUpdateView


class AccountsSignup(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/accounts_signup.html'


class AccountsUserDashboard(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'accounts/accounts_user_dashboard.html'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_type'] = 'Dashboard Home'

        return data


class AccountsUserDashboardProfileSettings(LoginRequiredMixin, MultiFormsView):
    login_url = '/login/'
    template_name = 'accounts/accounts_user_dashboard_profile_settings.html'
    form_classes = {
        'contact': forms.AccountsSetContactInformationForm,
        'user_image': forms.AccountsSetUserPhotographForm,
    }

    def user_image_form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse_lazy('accounts_user_dashboard_profile_settings', kwargs={'pk': self.request.user.id}))

    def contact_form_valid(self, form):
        form.save()
        return HttpResponseRedirect(
            reverse_lazy('accounts_user_dashboard_profile_settings', kwargs={'pk': self.request.user.id}))


class AccountsUserDashboardHistoricalTransactions(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'accounts/accounts_user_dashboard_historical_transactions.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_type'] = 'Historical Transactions'
        return data
