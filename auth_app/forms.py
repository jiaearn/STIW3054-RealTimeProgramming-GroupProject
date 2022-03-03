from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['ic','first_name','last_name']