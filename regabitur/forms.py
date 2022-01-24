from django import forms
from django.forms import SelectDateWidget, CheckboxSelectMultiple
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import ChoicesProfile, User, DocumentUser, CustomUser, AdditionalInfo


class MyLoginForm(AuthenticationForm, forms.ModelForm):
    """Форма для авторизации пользователей"""

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        """Переопределяем метод init для формы, чтобы задать нужные классы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-2'


class MyRegisterForm(forms.ModelForm):
    """Форма для регистрации пользователей"""

    class Meta:
        model = User
        fields = ('username',  'last_name', 'first_name', 'email', 'password')
        labels = {
            'username': ('Имя пользователя (Логин)'),
        }
        help_texts = {
            'username': ('',),
        }

    def __init__(self, *args, **kwargs):
        """Переопределяем метод init для формы, чтобы задать нужные классы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit = True):
        """переопределяем Save чтобы правильно сохранять пароли пользователей"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AddDocForm(forms.ModelForm):
    """Форма для добавления документов"""
    class Meta:
        model = DocumentUser
        fields = ('name_doc', 'doc')
        labels = {
            'name_doc': ('Тип документа', ),
        }

    def __init__(self, *args, **kwargs):
        """Переопределяем метод init для формы, чтобы задать нужные классы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mt-2 mb-3'


class AdditionalInfoForm(forms.ModelForm):
    """Форма для отправки профиля обучения"""
    class Meta:
        model = AdditionalInfo
        exclude = ['user']
        fields = ('education_profile', )
        widgets = {
            'education_profile': CheckboxSelectMultiple
        }


class AddInfoForm(forms.ModelForm):
    """форма для добавления и обнавления информации"""
    class Meta:
        model = CustomUser
        fields = ('date_of_birth', 'phone_number',  'passport', 'address',  'snils',
                  'name_uz', 'date_of_doc','patronymic',)
        widgets = {'snils': forms.TextInput(attrs={'mask': "999-999-999"})}

    def __init__(self, *args, **kwargs):
        """Переопределяем метод init для формы, чтобы задать нужные классы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['date_of_birth'].widget = SelectDateWidget(
                empty_label=("Выберите год", "Выберите месяц", "Выберите день"),
                years=range(1950, 2010))
            self.fields['date_of_birth'].widget.attrs['class'] = 'form-control mt-1'
            # self.fields['address'].widget.attrs['class'] = 'form-control'
            # self.fields['date_of_doc'].widget = SelectDateWidget(
            #     empty_label=("Выберите год", "Выберите месяц", "Выберите день"),
            #     years=range(1950, 2021))
            # self.fields['date_of_doc'].widget.attrs['class'] = 'form-control mt-1'
