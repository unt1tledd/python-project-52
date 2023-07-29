from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput, ModelForm, CharField
from task_manager.users.models import CustomUser
from django.core.exceptions import ValidationError


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'maxlength': '150'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию',
                'maxlength': '150'
            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя',
                'maxlength': '150'
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
                'maxlength': '150'
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Подтверждение пароля',
                'maxlength': '150'
            }),
        }
        
    def clean_username(self):
            username = self.cleaned_data.get("username")
            current_user_id = self.instance.id

            if username:
                user_exists = self._meta.model.objects.filter(
                    username__iexact=username
                ).exclude(id=current_user_id).exists()

                if user_exists:
                    self._update_errors(
                        ValidationError(
                            {
                                "username": self.instance.unique_error_message(
                                    self._meta.model, ["username"]
                                )
                            }
                        )
                    )
                else:
                    return username
