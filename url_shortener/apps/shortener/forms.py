from django import forms
from django.core.validators import FileExtensionValidator

from .models import Url


ACCEPTED_FORMATS = [
    'xlsx'
]


class UrlForm(forms.ModelForm):
    redirect_url = forms.URLField(
        required=True, error_messages={
            'invalid': '`redirect_url` პარამეტრი აუცილებელია.'
        }
    )
    tag = forms.CharField(
        required=True, error_messages={
            'invalid': '`tag` პარამეტრი აუცილებელია.'
        }
    )
    key = forms.CharField(required=False)
    expired = forms.CharField(required=False)

    class Meta:
        model = Url
        fields = ('redirect_url', 'tag', 'key', 'expired')


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='ფაილი', validators=[
            FileExtensionValidator(
                allowed_extensions=ACCEPTED_FORMATS,
                message='შესატვირთი ფაილის ფორმატი არასწორია, '
                        'დასაშვებია .xlsx ფორმატი'
            )
        ], error_messages={
            'invalid': 'ფაილის მიმაგრება აუცილებელია.'
        }, required=True
    )
