from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from . import models
# from widgets.custom_widgets import CustomImageWidget


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',)




# class MultipleForm(forms.Form):
#     action = forms.CharField(max_length=60, widget=forms.HiddenInput())


class AccountsSetContactInformationForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ('address', 'city', 'zip_code', 'country', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(AccountsSetContactInformationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# class AccountsSetBankAccountInformationForm(forms.ModelForm):
#     class Meta:
#         model = models.CustomUserFiatAccount
#         fields = ('account_first_name', 'account_last_name', 'account_nickname', 'account_number', 'routing_number')
#         labels = {
#             'account_first_name': 'Account First Name',
#             'account_last_name': 'Account Last Name',
#             'account_nickname': 'Account Nickname',
#             'account_number': 'Bank Account #',
#             'routing_number': 'Bank Account Routing #'
#         }
#
#         help_texts = {
#             'account_first_name': 'The first name listed on the account',
#             'account_last_name': 'The last name listed on the account',
#             'account_nickname': 'The nickname you want to associate to the account',
#             'account_number': 'The bank account number',
#             'routing_number': 'The bank account routing number'
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(AccountsSetBankAccountInformationForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'


class AccountsSetUserPhotographForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('user_image',)
        # widgets = {
        #     'user_image': CustomImageWidget
        # }

    def __init__(self, *args, **kwargs):
        super(AccountsSetUserPhotographForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
