from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from about.models import Trainer
from . models import *
from django.contrib.auth.hashers import make_password


class UserAuthenticationForm(forms.ModelForm):
    class Meta:
        fields = ['role', 'email', 'password']


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    # email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    widget = {
        'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if User.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # There has been changes
                if User.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")
        return formEmail

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if self.instance.pk is not None:
            if not password:
                # return None
                return self.instance.password

        return make_password(password)

    class Meta:
        model = User
        fields = ['role', 'name', 'email', 'password', ]


class TrainerForm(FormSettings):
    class Meta:
        model = Trainer
        fields = ['name', 'address', 'phone', 'email', 'ethnic', 'education', 'associated_organization_or_clinic',
        'area_of_expertise', 'experience', 'ege_group', 'province', 'district', 'municipality', 'ward', 'certification_from_mot', 'profile',
        'document', 'latitude', 'logitude']