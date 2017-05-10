from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


class UserForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_exists': _("Username already exists."),
        'email_exists': _("Email already exists."),
    }

    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    email = forms.EmailField(label=_('E-mail'))
    username = forms.CharField(
        label=_('Username'),
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[RegexValidator(
            r'[A-Za-z0-9@\.\+\-_]{1,30}',
            _('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
        )]
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    blog_name = forms.CharField(label=_('Blog name'))
    blog_description = forms.CharField(label=_('Blog description'))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        existent_users = User.objects.filter(username=username)
        if len(existent_users) > 0 and self.instance not in existent_users:
            raise ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existent_users = User.objects.filter(email=email)
        if len(existent_users) > 0 and self.instance not in existent_users:
            raise ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email.lower()

