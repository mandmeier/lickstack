from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    TS_CHOICES = [('0', 'concert key'), ('-3', 'Eb'), ('2', 'Bb')]
    instr_transpose_shift = forms.ChoiceField(
        choices=TS_CHOICES, initial='0', widget=forms.RadioSelect, label="Display and enter chords in")

    class Meta:
        model = Profile
        fields = ['instr_transpose_shift']
