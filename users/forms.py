from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core.mail import send_mail
from django.urls import reverse

from geekshop import settings
from users.models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите логин',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес эл. почты',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Повторите пароль',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        # making and sending confirm message to new user
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учётной записи GeekShop'
        message = f'Для подтверждения учётной записи {user.username} на сайте {settings.DOMAIN_NAME}, ' \
                  f'перейдите по следующей ссылке:\n<a href="{verify_link}">Активировать</a>'
        send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
    }), required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'username',
            'email',
        )


class UserProfileFormExtended(forms.ModelForm):

    # tagline = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    # }), required=False)
    #
    # about_me = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    # }), required=False)

    # gender = forms.ChoiceField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4',
    # }), required=False)

    class Meta:
        model = UserProfile
        fields = (
            'tagline',
            'about_me',
            'gender',
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileFormExtended, self).__init__(*args, **kwargs)

        user = UserProfile.objects.get(id=kwargs['instance'].id)
        self.initial['tagline'] = user.tagline
        self.initial['about_me'] = user.about_me
        self.initial['gender'] = user.gender

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = False
